from lib.db import db

class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    #item = db.relationship('Item', backref='category', uselist=False)

    def __init__(self, name):
        self.name = name