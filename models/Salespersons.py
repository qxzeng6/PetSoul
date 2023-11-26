from app import db


class Salespersons(db.Model):
    # table name
    __tablename__ = 'salespersons'

    salesperson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    phone = db.Column(db.CHAR(10))

    store_id = db.Column(db.Integer)

    name = db.Column(db.String(255))

    email = db.Column(db.String(255))

    street = db.Column(db.String(255))

    city = db.Column(db.String(255))

    state = db.Column(db.String(255))

    zipcode = db.Column(db.Integer)

    job_title = db.Column(db.String(255))

    salary = db.Column(db.Float(10, 2))

    def __init__(self, store_id, name, email, phone, street, city, state, zipcode, job_title, salary):
        self.store_id = store_id
        self.name = name
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.job_title = job_title
        self.salary = salary

    def __repr__(self):
        return '<Saleperson %r>' % self.name

    def __str__(self):
        return '<Saleperson %s>' % self.name
