from lib.db import db

class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.relationship('Category', uselist=False)
    #order = db.relationship('Order', backref='item', uselist=False)

    def __init__(self, category_id, name, price):
        self.category_id = category_id
        self.name = name
        self.price = price