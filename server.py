# import package
import bcrypt
from app import app, db, engine, product_Images
from models.User import User
from models.Customers import Customers
from models.Product import Product
from models.Transactions import Transactions
from models.Salespersons import Salespersons
from models.Store import Store
from models.Region import Region
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, send_file
import os
from sqlalchemy import create_engine
import toolbox.toolsForRegister as registerTool
import toolbox.toolsForaddItem as addItemTool
import toolbox.toolsForAddRegion as addRegionTool
import toolbox.toolsForAddStore as addStoreTool
import toolbox.toolsForAddSalesperson as addSalespersonTool
from werkzeug.exceptions import InternalServerError
from datetime import date
import uuid
from datetime import datetime


# # create Flask object as the application
# app = Flask(__name__)

# mapping the route to a python function


@app.route("/")
def welcomeGuest():
    # Drop a homepage in the templates called index.html, currently has no this html file
    # return render_template("index.html")
    return render_template("users.html")


@app.route("/register", methods=['GET', 'POST', 'OPTIONS'])
def register():
    print("user is registering!")
    if request.method == 'GET':
        return render_template("testRegister.html")
    elif request.method == 'POST':
        content = request.json
        UserInfoLst = registerTool.parseInfo(content)
        print("UserInfoLst: ", UserInfoLst)
        registerTool.dbUserInjector(UserInfoLst)
        return {"code": 0, "msg": "register success!"}
    else:
        return "is CORS working?"


@app.route('/user/<userName>', methods=["GET"])
def UserInfoProvider(userName):
    if userName == "ADMIN":
        admin_info = []
        return admin_info
    else:
        # return product_name, product_price, product_description, product_image
        product_Infos = db.select(Product.product_name, Product.price, Product.product_description,
                                  Product.image).where(Product.inventory_amount > 0)
        with engine.connect() as conn:
            result = conn.execute(
                product_Infos)

        print("result: ", result)
        return result


@app.route("/login", methods=['GET', 'POST', 'OPTIONS'])
def login():
    print("user is logging in!")
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        name = request.json.get('username')
        password = request.json.get('password')
        print(name)
        print(type(password), password)
        customer = Customers.query.filter_by(user_name=name).first()
        if customer is None:
            return "there has no such user!"

        # print("customer: ", customer)
        bytePassword = password.encode('utf-8')
        # print("bytePassword: ", bytePassword)
        print(type(customer.password))
        if customer and bcrypt.checkpw(bytePassword, customer.password.encode('utf-8')):
            return {"code": 0, "msg": "login success!"}
        else:
            return {"code": 1, "msg": "login failed!"}
    else:
        return "is CORS working?"


@app.route("/user/<userName>/update", methods=["POST", "OPTIONS", "GET"])
def UserInfoUpdater(userName):
    if userName == "ADMIN":
        return 0
    else:
        return 1


@app.route('/upload/product_Images/<filename>', methods=['GET'])
def get_image(filename):
    print("uploading image!")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print("filepath: ", filepath)
    # Check if the file exists
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/jpeg')
    else:
        return {'error': 'Image not found'}, 404


@app.route("/purchase", methods=["GET"])
def UserPurchase():
    userName = request.args.get("username")
    product_id = request.args.get("product_id")
    buy_amount = request.args.get("buy_number")
    print("product_id: ", product_id)
    product_to_update = Product.query.get(product_id)
    print("product_to_update: ", product_to_update)
    if product_to_update and userName is not None and userName != "":
        if product_to_update.inventory_amount <= buy_amount:
            return {"code": 1, "msg": "sold out!"}

        product_to_update.inventory_amount = product_to_update.inventory_amount - buy_amount
        product_to_update.sold_quantity = product_to_update.sold_quantity + buy_amount
        # product_to_update.sold_amount = product_to_update.sold_amount + product_to_update.price
        # db.session.commit()
    else:
        return {"code": 1, "msg": "product or user not found!"}

    customer = Customers.query.filter_by(user_name=userName).first()
    if customer is None:
        return {"code": 1, "msg": "User Not Found!"}
    customer_id = customer.customer_id
    print("customer_id: ", customer_id)
    salesperson_id = product_to_update.saleperson_id
    print("salesperson_id: ", salesperson_id)
    store_id = Salespersons.query.filter_by(salesperson_id=salesperson_id).first().store_id
    print("store_id: ", store_id)
    region_id = Store.query.filter_by(store_id=store_id).first().region_id
    if region_id is not None:
        targetRegion = Region.query.filter_by(region_id=region_id).first()
        targetRegion.sold_amount = targetRegion.sold_amount + product_to_update.price * buy_amount
        targetRegion.sold_quantity = targetRegion.sold_quantity + buy_amount
        # db.session.commit()

    salesperson_name = Salespersons.query.get(salesperson_id).name
    print("salesperson_name: ", salesperson_name)
    order_num = generate_order_number()
    transaction = Transactions(customer_id=customer_id, product_id=product_id, store_id=store_id,
                               salesperson_id=salesperson_id, order_number=order_num, date=date.today(),
                               salesperson_name=salesperson_name, product_number=1)
    db.session.add(transaction)
    db.session.commit()
    return {"code": 0, "msg": "purchase success!"}


def generate_order_number():
    timestamp = int(datetime.utcnow().timestamp() * 1000)  # Convert to milliseconds
    unique_id = uuid.uuid4().hex[:8]  # Use the first 8 characters of a UUID

    orderNum = f"{timestamp}-{unique_id}"
    return orderNum


# developing
@app.route("/addregion", methods=["POST", "OPTIONS"])
def addRegion():
    if request.method == "POST":
        print("ADMIN is adding region!")
        # print("content :", request.json)
        content = request.form
        print("content: ", content)
        if content == "" or content is None:
            return "no file!"
        else:
            regionInfoLst = addRegionTool.parseRegionInfo(content)
            addRegionTool.regionDBAdder(regionInfoLst)
            return {"code": 0, "msg": "Region add success!"}

    else:
        return "is CORS working?"


@app.route("/addsaleperson", methods=["POST", "OPTIONS"])
def addSalesperson():
    if request.method == "POST":
        print("ADMIN is adding salesperson!")
        # print("content :", request.json)
        content = request.form
        print("content: ", content)
        if content == "" or content is None:
            return "no file!"
        else:
            salespersonInfoLst = addSalespersonTool.parseSalespersonInfo(content)
            addSalespersonTool.salespersonDBAdder(salespersonInfoLst)
            return {"code": 0, "msg": "Salesperson add success!"}

    else:
        return "is CORS working?"


@app.route("/addstore", methods=["POST", "OPTIONS"])
def addStore():
    if request.method == "POST":
        print("ADMIN is adding store!")
        # print("content :", request.json)
        content = request.form
        print("content: ", content)
        if content == "" or content is None:
            return "no file!"
        else:
            storeInfoLst = addStoreTool.parseStoreInfo(content)
            addStoreTool.storeDBAdder(storeInfoLst)
            return {"code": 0, "msg": "Store add success!"}

    else:
        return "is CORS working?"


@app.route("/add", methods=["POST", "OPTIONS"])
def requestParser():
    if request.method == "POST":
        print("ADMIN is adding item!")
        # print("content :", request.json)
        imagefile = request.files.get('file', '')
        content = request.form
        print("imagefile: ", imagefile)
        if content == "":
            return "no file!"
        if content:
            productInfoLst = addItemTool.parseInfo(content, imagefile)
            ItemAdder(productInfoLst)
            return "add item success!"
        return "developing..."
    else:
        return "is CORS working?"


def ItemAdder(productInfoLst: list):
    newProduct = Product(productInfoLst[0], productInfoLst[1], productInfoLst[2], productInfoLst[3], productInfoLst[4],
                         productInfoLst[5], 0, productInfoLst[6])
    db.session.add(newProduct)
    db.session.commit()
    return


@app.route("/list", methods=["GET"])
def listAllProductInfo():
    print("listing target products info")
    product_id = request.args.get("product_id")
    print("product_id: ", product_id)
    product_name = request.args.get("product_name")
    print("product_name: ", product_name)
    products = Product.query
    columns = Product.__table__.columns.keys()
    if product_id is not None and product_id != "":
        products = products.filter_by(product_id=product_id)

    if product_name is not None and product_name != "":
        products = products.filter_by(product_name=product_name)
    products = products.all()

    products_dict_list = [{column: getattr(product, column) for column in columns} for product in products]
    return {"code": 200, "msg": "success",
            "data": {"content": products_dict_list, "totalElement": len(products_dict_list)}}


@app.route("/transactionlist", methods=["GET"])
def listAllTransactionInfo():
    print("listing target transaction info")
    transaction_id = request.args.get("id")
    print("transaction_id: ", transaction_id)
    store_id = request.args.get("store_id")
    print("store_id: ", store_id)
    region_id = request.args.get("region_id")
    transactions = Transactions.query
    columns = Transactions.__table__.columns.keys()
    if transaction_id is not None and transaction_id != "":
        transactions = transactions.filter_by(id=transaction_id)
    if store_id is not None and store_id != "":
        transactions = transactions.filter_by(store_id=store_id)
    if region_id is not None and region_id != "":
        transactions = transactions.filter_by(region_id=region_id)
    transactions = transactions.all()
    transactions_dict_list = [{column: getattr(transaction, column) for column in columns} for transaction in
                              transactions]
    return {"code": 200, "msg": "success",
            "data": {"content": transactions_dict_list, "totalElement": len(transactions_dict_list)}}


@app.route("/orderlist", methods=["GET"])
def listTargetOrderInfo():
    print("list target order info")
    order_id = request.args.get("id")
    user_name = request.args.get("username")
    TargetUser = Customers.query.filter_by(user_name=user_name).first()
    user_id = TargetUser.customer_id
    orders = Transactions.query
    if order_id is not None and order_id != "":
        orders = orders.filter_by(id=order_id)
    if user_id is not None and user_id != "":
        print("user_id: ", user_id)
        orders = orders.filter_by(customer_id=user_id)
    print("orders: ", orders)
    orders = orders.all()
    print("orders: ", orders)
    columns = Transactions.__table__.columns.keys()
    orders_dict_list = [{column: getattr(order, column) for column in columns} for order in orders]
    print("orders_list_of_lists: ", orders_dict_list)
    return {"code": 200, "msg": "success",
            "data": {"content": orders_dict_list, "totalElement": len(orders_dict_list)}}


@app.route("/userlist", methods=["GET"])
def listTargetUserInfo():
    print("list target user info")
    customer_id = request.args.get("customer_id")
    print("customer_id: ", customer_id)
    user_name = request.args.get("customer_name")
    print("user_name: ", user_name)
    kind = request.args.get("kind")
    print("kind: ", kind)
    customers = Customers.query
    columns = Customers.__table__.columns.keys()
    if customer_id is not None and customer_id != "":
        customers = customers.filter_by(customer_id=customer_id)

    if user_name is not None and user_name != "":
        print("user_name: ", user_name)
        customers = customers.filter_by(user_name=user_name)

    if kind is not None and kind != "":
        customers = customers.filter_by(kind=kind)

    customers = customers.all()
    print("customers: ", customers)
    customers_dict_list = [{column: getattr(customer, column) for column in columns} for customer in customers]
    # print("customers_dict_list: ", customers_dict_list)
    res_dict = {"code": 200, "msg": "success",
                "data": {"content": customers_dict_list, "totalElement": len(customers_dict_list)}}
    return res_dict


@app.route("/storelist", methods=["GET"])
def listTargetStoreInfo():
    store_id = request.args.get("store_id")
    print("store_id: ", store_id)
    region_id = request.args.get("region_id")
    print("region_id: ", region_id)
    stores = Store.query
    columns = Store.__table__.columns.keys()
    if store_id is not None and store_id != "":
        stores = stores.filter_by(store_id=store_id)
    if region_id is not None and region_id != "":
        stores = stores.filter_by(region_id=region_id)
    stores = stores.all()
    stores_dict_list = [{column: getattr(store, column) for column in columns} for store in stores]
    return {"code": 200, "msg": "success",
            "data": {"content": stores_dict_list, "totalElement": len(stores_dict_list)}}


@app.route("/regionlist", methods=["GET"])
def listAllRegionInfo():
    print("listing all region info")
    region_id = request.args.get("region_id")
    regions = Region.query
    columns = Region.__table__.columns.keys()
    if region_id is not None and region_id != "":
        regions = regions.filter_by(region_id=region_id)
    regions = regions.all()
    regions_dict_list = [{column: getattr(region, column) for column in columns} for region in regions]
    return {"code": 200, "msg": "success",
            "data": {"content": regions_dict_list, "totalElement": len(regions_dict_list)}}


@app.route("/salepersonlist", methods=["GET"])
def listAllSalespersonInfo():
    print("listing all salesperson info")
    salesperson_id = request.args.get("saleperson_id")
    region_id = request.args.get("region_id")
    job_title = request.args.get("job_title")
    salespersons = Salespersons.query
    columns = Salespersons.__table__.columns.keys()
    if salesperson_id is not None and salesperson_id != "":
        salespersons = salespersons.filter_by(salesperson_id=saleperson_id)
    if region_id is not None and region_id != "":
        salespersons = salespersons.filter_by(store_id=region_id)
    if job_title is not None and job_title != "":
        salespersons = salespersons.filter_by(job_title=job_title)
    salespersons = salespersons.all()
    salespersons_dict_list = [{column: getattr(salesperson, column) for column in columns} for salesperson in
                              salespersons]

    return {"code": 200, "msg": "success",
            "data": {"content": salespersons_dict_list, "totalElement": len(salespersons_dict_list)}}


@app.route("/productlist", methods=["GET"])
def listAllProductInfo_Index():
    print("listing all product info")
    product_name = request.args.get("product_name")
    products = Product.query
    columns = Product.__table__.columns.keys()
    if product_name is not None and product_name != "":
        products = products.filter_by(product_name=product_name)
    products = products.all()
    products_dict_list = [{column: getattr(product, column) for column in columns} for product in products]
    return {"code": 200, "msg": "success",
            "data": {"content": products_dict_list, "totalElement": len(products_dict_list)}}


@app.errorhandler(Exception)
def handle_500_error(e):
    print("error :", e)
    resp = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    # set 'debug = true' allows to restart application when saving a file
    app.run(host='0.0.0.0', port=8080, debug=True)
