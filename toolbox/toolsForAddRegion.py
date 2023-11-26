import flask
from models.Product import Product
from models.Region import Region
from app import app, db, engine
import os


def parseRegionInfo(content):
    region_name = content.get('region_name')
    print("region_name: ", region_name)
    region_manager = content.get('region_manager')
    print("region_manager: ", region_manager)
    store_number = content.get('storenum')
    print("store_number: ", store_number)
    sold_amount = content.get('soldamount')
    print("sold_amount: ", sold_amount)
    sold_quantity = content.get('soldquantity')
    print("sold_quantity: ", sold_quantity)

    return [region_name, region_manager, store_number, sold_amount, sold_quantity]


def regionDBAdder(regionInfoLst: list):
    newRegion = Region(regionInfoLst[0], regionInfoLst[1], regionInfoLst[2], regionInfoLst[3], regionInfoLst[4])

    db.session.add(newRegion)
    db.session.commit()
    return
