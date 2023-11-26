from models.Customers import Customers
import bcrypt
from app import app, db, engine


def parseInfo(registrationInfo):
    customer_name = registrationInfo.get('customer_name')
    user_name = registrationInfo.get('user_name')
    password = registrationInfo.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    email = registrationInfo.get('email')

    phone_number = registrationInfo.get('phone_number')
    street = registrationInfo.get('street')
    city = registrationInfo.get('city')
    state = registrationInfo.get('state')
    zip_code = registrationInfo.get('zip_code')

    kind = registrationInfo.get('kind')
    business_category = registrationInfo.get('business_category')
    annual_income = registrationInfo.get('annual_income')
    if annual_income == "" or annual_income is None:
        annual_income = 0
    gender = registrationInfo.get('gender')
    age = registrationInfo.get('age')
    if age == "" or age is None:
        age = 0
    income = registrationInfo.get('income')
    if income == "" or income is None:
        income = 0
    marriage = registrationInfo.get('marriage')
    date_of_birth = registrationInfo.get('date_of_birth')
    pet_kind = registrationInfo.get('pet_kind')
    return [customer_name, user_name, hashed_password, email, phone_number, street, city, state, zip_code, kind,
            business_category, annual_income, gender, age, income, marriage, date_of_birth, pet_kind]


def dbUserInjector(userInfoLst: list):
    newCustomer = Customers(userInfoLst[0], userInfoLst[1], userInfoLst[2], userInfoLst[3], userInfoLst[4],
                            userInfoLst[5], userInfoLst[6], userInfoLst[7], userInfoLst[8], userInfoLst[9],
                            userInfoLst[10], userInfoLst[11], userInfoLst[12], userInfoLst[13], userInfoLst[14],
                            userInfoLst[15], userInfoLst[16], userInfoLst[17])
    db.session.add(newCustomer)
    db.session.commit()
    return
