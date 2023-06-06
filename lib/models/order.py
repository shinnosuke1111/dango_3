from lib.db import db
from datetime import datetime

class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item_num = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    customer = db.relationship('Customer', uselist=False)
    item = db.relationship('Item', uselist=False)

    def __init__(self, customer_id, item_id, item_num, total_price):
        self.customer_id = customer_id
        self.item_id =  item_id
        self.item_num = item_num 
        self.total_price = total_price
        self.order_date = datetime.today()