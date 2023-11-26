from app import app, db, engine
from models.Salespersons import Salespersons


def parseSalespersonInfo(content):
    store_id = content.get('store_id')
    print("store_id: ", store_id)
    parent_store = Store.query.filter_by(store_id=store_id).first()
    print("parent_store: ", parent_store)
    if parent_store is not None:
        print("parent_store.number_of_salespersons: ", parent_store.number_of_salespersons)
        parent_store.number_of_salespersons += 1
        db.session.commit()

    name = content.get('name')
    print("name: ", name)
    email = content.get('email')
    print("email: ", email)
    phone = content.get('phone')
    print("phone: ", phone)
    street = content.get('street')
    print("street: ", street)
    city = content.get('city')
    print("city: ", city)
    state = content.get('state')
    print("state: ", state)
    zipcode = content.get('zipcode')
    print("zipcode: ", zipcode)
    job_title = content.get('job_title')
    print("job_title: ", job_title)
    salary = content.get('salary')
    print("salary: ", salary)

    return [store_id, name, email, phone, street, city, state, zipcode, job_title, salary]


def salespersonDBAdder(salespersonInfoLst: list):
    newSalesperson = Salespersons(salespersonInfoLst[0], salespersonInfoLst[1], salespersonInfoLst[2],
                                  salespersonInfoLst[3], salespersonInfoLst[4],
                                  salespersonInfoLst[5], salespersonInfoLst[6], salespersonInfoLst[7],
                                  salespersonInfoLst[8], salespersonInfoLst[9])

    db.session.add(newSalesperson)
    db.session.commit()
    return
