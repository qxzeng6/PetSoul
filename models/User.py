from app import db


class User(db.Model):
    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(64), unique=True, index=True)

    pwd = db.Column(db.String(64), default=0)

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd

    def __repr__(self):
        return '<User %r>' % self.name

    def __str__(self):
        return '<User %s>' % self.name
