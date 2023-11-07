from app import db


class Product(db.Model):
    # table name
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    product_name = db.Column(db.String(255))

    price = db.Column(db.Float(10,2))

    inventory_amount = db.Column(db.Integer)

    product_kind = db.Column(db.String(255))

    product_description = db.Column(db.String(255))

    sold_quantity = db.Column(db.Integer)

    image = db.Column(db.String(500))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Product %r>' % self.name

    def __str__(self):
        return '<Product %s>' % self.name
