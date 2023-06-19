from lib.db import db
class Message(db.Model):
    __tablename__ = 'message'
    tweet_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'))
    message = db.Column(db.String())
    account = db.relationship("Account", uselist=False)
    
def __init__(self, message):
    self.message = message