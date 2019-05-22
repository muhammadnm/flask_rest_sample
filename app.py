from flask import Flask, request, jsonify
from models import db, Product
from schemas import ma, ProductSchema
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB & Marshmallow
db.init_app(app)
ma.init_app(app)

prod_schema = ProductSchema(strict=True)
prods_schema = ProductSchema(many=True, strict=True)

# Create a new product
@app.route('/products', methods=['POST'])
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  new_product = Product(name, description, price, qty)

  db.session.add(new_product)
  db.session.commit()

  return jsonify(msg='Product ['+ new_product.name +'] created successfully'), 200

# Get All Products
@app.route('/products', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = prods_schema.dump(all_products)
  return jsonify(err=False, data=result.data), 200

# Get Single Products
@app.route('/products/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)

  if product is None:
    return jsonify(err=True, msg='Invalid request, product not found'), 200
  else:
    # print('product', product.serialize)
    return jsonify(err=False, data=product.serialize), 200

# Update a Product
@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  if product is None:
    return jsonify(err=True, msg='Invalid request, product not found'), 200
  else:
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()
    return jsonify(err=False, msg='Product updated successfully'), 200

# Delete Product
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  
  if product is None:
    return jsonify(err=True, msg='Invalid request, product not found'), 200
  else:
    db.session.delete(product)
    db.session.commit()

    return jsonify(err=False, msg=product.name + ' deleted successfully'), 200

# Run server
if __name__ == '__main__':
    app.run(debug=True)