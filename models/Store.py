from app import db


class Store(db.Model):
    # table name
    __tablename__ = 'store'

    store_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    store_name = db.Column(db.String(255))

    region_id = db.Column(db.Integer)

    manager = db.Column(db.String(255))

    street = db.Column(db.String(255))

    city = db.Column(db.String(255))

    state = db.Column(db.String(255))

    zip_code = db.Column(db.Integer)

    number_of_salespersons = db.Column(db.Integer)

    def __init__(self, region_id, store_name, manager, street, city, state, zip_code,
                 number_of_salespersons):
        self.region_id = region_id
        self.store_name = store_name
        self.manager = manager
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.number_of_salespersons = number_of_salespersons

    def __repr__(self):
        return '<Store %r>' % self.store_name

    def __str__(self):
        return '<Store %s>' % self.store_name
