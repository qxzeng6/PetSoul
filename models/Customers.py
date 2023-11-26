from app import db


class Customers(db.Model):
    # table name
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    customer_name = db.Column(db.String(255))

    user_name = db.Column(db.String(255))

    password = db.Column(db.String(255))

    email = db.Column(db.String(255))

    phone_number = db.Column(db.String(255))

    street = db.Column(db.String(255))

    city = db.Column(db.String(255))

    state = db.Column(db.String(255))

    zip_code = db.Column(db.String(10))

    kind = db.Column(db.Integer)  # 1 for business user, 0 for home user

    business_category = db.Column(db.String(255))

    annual_income = db.Column(db.Float(10, 2))

    gender = db.Column(db.String(10))

    age = db.Column(db.Integer)

    income = db.Column(db.Float(10, 2))

    marriage = db.Column(db.String(20))

    date_of_birth = db.Column(db.Date)

    pet_kind = db.Column(db.String(255))

    def __init__(self,customer_name, user_name, password, email, phone_number, street, city, state, zip_code, kind,
                 business_category, annual_income,gender,age,income,marriage,date_of_birth,pet_kind):
        self.customer_name = customer_name
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.kind = kind
        self.business_category = business_category
        self.annual_income = annual_income
        self.gender = gender
        self.age = age
        self.income = income
        self.marriage = marriage
        self.date_of_birth = date_of_birth
        self.pet_kind = pet_kind
        return

    def __repr__(self):
        return '<Customer %r>' % self.user_name

    def __str__(self):
        return '<Customer %s>' % self.user_name
