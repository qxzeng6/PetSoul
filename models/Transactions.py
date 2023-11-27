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

    def __init__(self, customer_id, product_id, store_id, salesperson_id, order_number, date, salesperson_name, product_number):
        self.customer_id = customer_id
        self.product_id = product_id
        self.store_id = store_id
        self.salesperson_id = salesperson_id
        self.order_number = order_number
        self.date = date
        self.salesperson_name = salesperson_name
        self.product_number = product_number

        return

    def __repr__(self):
        return '<Transaction %r>' % self.id

    def __str__(self):
        return '<Transaction %s>' % self.id
