from app import db


class Store(db.Model):
    # table name
    __tablename__ = 'store'

    store_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    salesperson_id = db.Column(db.Integer)

    region_id = db.Column(db.Integer)

    store_name = db.Column(db.String(255))

    address = db.Column(db.String(255))

    manager = db.Column(db.String(255))

    number_of_salespersons = db.Column(db.Integer)