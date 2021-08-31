from os import name
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True)
    price=db.Column(db.Float)
    qty=db.Column(db.Integer)


    def __init__(self,name,price,qty):
        self.name=name
        self.price=price
        self.qty=qty

class ProductSchema(ma.Schema):
    class Meta:
        fields=('id','name','price','qty')


product_schema = ProductSchema()
products_schema =ProductSchema(many=True)

@app.route('/',methods=['POST'])
def add_product():
    name= request.json['name']
    price= request.json['price']
    qty= request.json['qty']
    new_product =Product(name=name,price=price,qty=qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


@app.route('/get',methods=['GET'])
def get_products():
    all_products=Product.query.all()
    result =products_schema.dump(all_products)
    return jsonify(result)

@app.route('/<id>',methods=['GET'])
def get_particular(id):
    paarticular_prod= Product.query.get(id)
    return product_schema.jsonify(paarticular_prod)

@app.route('/prod_update/<id>',methods=['PUT'])
def prod_update(id):
    prod=Product.query.get(id)

    name= request.json['name']
    price= request.json['price']
    qty= request.json['qty']

    prod.name= name
    prod.price= price
    prod.qty= qty

    db.session.commit()
    return product_schema.jsonify(prod)

@app.route('/prod_delete/<id>', methods=['DELETE'])
def prod_delete(id):
    delete=Product.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return product_schema.jsonify(delete)


if __name__=="__main__":        
   app.run(debug=True)        


