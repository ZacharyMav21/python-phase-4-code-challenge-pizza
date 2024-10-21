#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = [{
        'id': r.id,
        'name': r.name,
        'address': r.address
    } for r in Restaurant.query.all()]
    return restaurants, 200

@app.route("/restaurants/<int:id>", methods=["GET", "DELETE"])
def restaurant_details(id):
    restaurant = db.session.get(Restaurant, id)
    if request.method == "GET":
        if restaurant:
            return restaurant.to_dict(), 200
        return {"error": "Restaurant not found"}, 404

    if request.method == "DELETE":
       if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204
    return {"error": "Restaurant not found"}, 404
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = [{
        'id': p.id,
        'name': p.name,
        'ingredients': p.ingredients
    } for p in Pizza.query.all()]
    return pizzas, 200

# Create new restaurant pizza
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    restaurant_id = data.get('restaurant_id')
    pizza_id = data.get('pizza_id')
    getpizza = Pizza.query.get(pizza_id)
    getrestaurant = Restaurant.query.get(restaurant_id)
    if getrestaurant:
        if getpizza:
            if price >= 1 and price <= 30:
                create = RestaurantPizza(price=price,pizza_id=pizza_id,restaurant_id=restaurant_id)
                db.session.add(create)
                db.session.commit()
                return create.to_dict(), 201
            else:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400    
    else:
        return {"errors": ["validation errors"]}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)