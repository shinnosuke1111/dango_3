from lib.db import db

class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    #order = db.relationship('Order', backref='customer', uselist=False)

    def __init__(self, name, address, tel, email):
        self.name = name
        self.address = address
        self.tel = tel
        self.email = email