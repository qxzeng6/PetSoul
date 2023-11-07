from app import db


class Customers(db.Model):
    # table name
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    customer_name = db.Column(db.String(255))

    user_name=db.Column(db.String(255))

    password = db.Column(db.String(255))

    email = db.Column(db.String(255))

    phone_number = db.Column(db.String(255))

    street = db.Column(db.String(255))

    city = db.Column(db.String(255))

    state = db.Column(db.String(255))

    zip_code = db.Column(db.String(10))

    kind = db.Column(db.Integer)  #1 for business user, 0 for home user

    business_category = db.Column(db.String(255))

    annual_income = db.Column(db.Float(10, 2))

    gender = db.Column(db.String(10))

    age = db.Column(db.Integer)

    income = db.Column(db.Float(10, 2))

    marriage = db.Column(db.String(20))

    date_of_birth = db.Column(db.Date)

    pet_kind = db.Column(db.String(255))

    def __init__(self):
        return


    def __repr__(self):
        return '<Product %r>' % self.name

    def __str__(self):
        return '<Product %s>' % self.name
