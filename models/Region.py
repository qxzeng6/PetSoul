from app import db


class Region(db.Model):
    # table name
    __tablename__ = 'region'

    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    region_name = db.Column(db.String(255))

    region_manager = db.Column(db.String(255))

    store_number = db.Column(db.Integer)

    sold_amount = db.Column(db.Integer)

    sold_quantity = db.Column(db.Integer)

    def __init__(self, region_name, region_manager, store_number, sold_amount, sold_quantity):
        self.region_name = region_name
        self.region_manager = region_manager
        self.store_number = store_number
        self.sold_amount = sold_amount
        self.sold_quantity = sold_quantity

    def __repr__(self):
        return '<Region %r>' % self.region_name

    def __str__(self):
        return '<Region %s>' % self.region_name
