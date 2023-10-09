#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    return '<h1>Bakery GET API</h1>'

@app.route("/bakeries", methods = ['GET'])
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in bakeries]

    return jsonify(bakery_list)


@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    query = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = {
            'id': query.id,
            'name': query.name,
            'created_at': query.created_at
        }
    response = make_response(jsonify(bakery_dict), 200)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    query = BakedGood.query.order_by((BakedGood.price).desc())
    listofbakedgoods = []
    for bakedgood in query:
        dict = {
            'id': bakedgood.id,
            'name': bakedgood.name,
            'price': bakedgood.price,
            'created_at': bakedgood.created_at
            }
        listofbakedgoods.append(dict)
    return listofbakedgoods

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    query = BakedGood.query.order_by((BakedGood.price).desc()).first()
    dict = {
            'id': query.id,
            'name': query.name,
            'price': query.price,
            'created_at': query.created_at
            }
    return make_response(dict, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
