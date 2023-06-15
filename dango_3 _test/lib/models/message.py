from lib.db import db

class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    message = db.Column(db.String())


def __init__(self, message, name):
    self.message = message
    self.name = name
    