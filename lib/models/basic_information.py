from lib.db import db

class Basic_information(db.Model):

    __tablename__ = 'basic_information'


    basic_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'))
    birth_month = db.Column(db.String(2))
    birth_day = db.Column(db.String(2))
    team = db.Column(db.String(64))
    hobby = db.Column(db.String(64))
    word = db.Column(db.String(64))

def __init__(self, birth_month, birth_day, team = '---', hobby = '---', word = '宜しくお願いします。'):
    self.birth_month = birth_month
    self.birth_day = birth_day
    self.team = team
    self.hobby = hobby
    self.word = word