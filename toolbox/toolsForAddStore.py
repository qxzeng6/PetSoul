from models.Store import Store
from app import app, db, engine
from models.Region import Region


def parseStoreInfo(content):
    store_name = content.get('store_name')
    print("store_name: ", store_name)
    region_id = content.get('region_id')
    print("region_id: ", region_id)
    parent_region = Region.query.filter_by(region_id=region_id).first()
    print("parent_region: ", parent_region)
    if parent_region is not None:
        print("parent_region.store_number: ", parent_region.store_number)
        parent_region.store_number += 1
        db.session.commit()

    manager = content.get('manager')
    print("store_manager: ", manager)
    street = content.get('street')
    print("store_address: ", street)
    city = content.get('city')
    print("store_city: ", city)
    state = content.get('state')
    print("store_state: ", state)
    zip_code = content.get('zipcode')
    print("store_zip_code: ", zip_code)
    number_of_salespersons = content.get('number_of_salepersons')
    print("number_of_salespersons: ", number_of_salespersons)

    return [region_id, store_name, manager, street, city, state, zip_code, number_of_salespersons]


def storeDBAdder(storeInfoLst: list):
    newStore = Store(storeInfoLst[0], storeInfoLst[1], storeInfoLst[2], storeInfoLst[3], storeInfoLst[4],
                     storeInfoLst[5], storeInfoLst[6], storeInfoLst[7])

    db.session.add(newStore)
    db.session.commit()
    return
