from app import db


class Transactions(db.Model):
    # table name
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    customer_id = db.Column(db.Integer)

    product_id = db.Column(db.Integer)

    store_id = db.Column(db.Integer)

    salesperson_id = db.Column(db.Integer)

    order_number = db.Column(db.String(255))

    date = db.Column(db.Date)

    salesperson_name = db.Column(db.String(255))

    product_number = db.Column(db.Integer)

    def __init__(self):
        return


    def __repr__(self):
        return '<Product %r>' % self.name

    def __str__(self):
        return '<Product %s>' % self.name