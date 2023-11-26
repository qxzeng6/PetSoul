import flask
from models.Product import Product
from app import app, db, engine
import os


def parseInfo(content,imageContent):
    product_name = content.get('product_name')
    print("product_name: ", product_name)
    product_price = content.get('price')
    print("product_price: ", product_price)
    saleperson_id = int(content.get('saleperson_id'))
    print("saleperson_id: ", saleperson_id)
    inventory_amount = content.get('inventory_amount')
    print("inventory_amount: ", inventory_amount)
    product_kind = content.get('product_kind')
    print("product_kind: ", product_kind)
    product_description = content.get('product_description')
    print("product_description: ", product_description)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], product_name + '.jpg')
    print("filePath: ", filePath)
    imageContent.save(filePath)
    return [product_name, product_price, saleperson_id,inventory_amount, product_kind, product_description, filePath]
