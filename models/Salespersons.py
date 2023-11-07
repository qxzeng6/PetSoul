from app import db


class Salespersons(db.Model):
    # table name
    __tablename__ = 'salespersons'

    salesperson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    store_id = db.Column(db.Integer)

    name = db.Column(db.String(255))

    address = db.Column(db.String(255))

    email = db.Column(db.String(255))

    job_title = db.Column(db.String(255))

    salary = db.Column(db.Float(10, 2))


    def __init__(self):
        return


    def __repr__(self):
        return '<Product %r>' % self.name

    def __str__(self):
        return '<Product %s>' % self.name