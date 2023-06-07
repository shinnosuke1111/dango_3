from lib.db import db

class Account(db.Model):


    __tablename__ = 'account'


    account_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    ruby = db.Column(db.String(64), nullable=False)
    dept = db.Column(db.String(64), nullable=False)
    group = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer(4), nullable=False)
    
    def __init__(self, account_id, email, password, name, ruby, dept, group, year):
        self.account_id = account_id
        self.email = email
        self.password = password
        self.name = name
        self.ruby = ruby
        self.dept = dept
        self.group = group
        self.year = year
