from flask_sqlalchemy import SQLAlchemy

# Init DB
db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer)
    
    @property
    def serialize(self):
       return {
           'id' : self.id,
           'name': self.name,
           'desc': self.desc,
           'price': self.price,
           'qty': self.qty
       }

    def __init__(self, name, desc, price, qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty
