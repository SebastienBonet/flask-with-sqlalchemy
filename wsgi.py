# wsgi.py
from flask import Flask, jsonify, request
from config import Config
import pdb

app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/')
def hello():
    return "Hello World! I present to you an API"

@app.route('/products', methods=['GET'])
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    db.session.commit()
    return products_schema.jsonify(products)

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = db.session.query(Product).get(id)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<id>', methods=['GET', 'POST'])
def ins_product(id):
    new_product_dict = request.get_json()
    new_product_name = new_product_dict.get('name')
    new_product = Product(id = id, name = new_product_name)
    db.session.add(new_product)
    db.session.commit()
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    db.session.commit()
    return products_schema.jsonify(products)

@app.route('/products/<id>', methods=['DELETE'])
def del_product(id):
    product = db.session.query(Product).get(id)
    db.session.delete(product)
    db.session.commit()
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    db.session.commit()
    return products_schema.jsonify(products)

@app.route('/products/<id>', methods=['PATCH'])
def upd_product(id):
    new_product_dict = request.get_json()
    new_product_name = new_product_dict.get('name')
    product = db.session.query(Product).get(id)
    product.name = new_product_name
    db.session.commit()
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    db.session.commit()
    return products_schema.jsonify(products)


