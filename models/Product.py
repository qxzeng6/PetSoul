from app import db


class Product(db.Model):
    # table name
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    product_name = db.Column(db.String(255))

    price = db.Column(db.Numeric(10, 2))

    saleperson_id = db.Column(db.Integer)

    inventory_amount = db.Column(db.Integer)

    product_kind = db.Column(db.String(255))

    product_description = db.Column(db.String(255))

    sold_quantity = db.Column(db.Integer)

    image = db.Column(db.String(500))

    def __init__(self, product_name, price, salepersion_id,inventory_amount, product_kind, product_description, sold_quantity, image):
        self.product_name = product_name
        self.price = price
        self.saleperson_id = salepersion_id
        self.inventory_amount = inventory_amount
        self.product_kind = product_kind
        self.product_description = product_description
        self.sold_quantity = sold_quantity
        self.image = image

    def __repr__(self):
        return '<Product %r>' % self.product_name

    def __str__(self):
        return '<Product %s>' % self.product_name
