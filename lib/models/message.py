from lib.db import db
class Message(db.Model):
    __tablename__ = 'message'
    tweet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    message = db.Column(db.String())
    
def __init__(self, message, name):
    self.tweet_id = tweet_id
    self.message = message
    self.name = name