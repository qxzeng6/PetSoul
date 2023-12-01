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
from sqlalchemy import create_engine, func
import toolbox.toolsForRegister as registerTool
import toolbox.toolsForaddItem as addItemTool
import toolbox.toolsForAddRegion as addRegionTool
import toolbox.toolsForAddStore as addStoreTool
import toolbox.toolsForAddSalesperson as addSalespersonTool
from werkzeug.exceptions import InternalServerError
from datetime import date
import uuid
from datetime import datetime


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


@app.route("/productdetail", methods=["GET"])
def ProductDetailProvider():
    if request.method == "GET":
        product_id = request.args.get("product_id")
        print("product_id: ", product_id)
        product = Product.query.filter_by(product_id=product_id).first()
        if product is None:
            return {"code": 404, "msg": "no such product!"}
        else:
            product_dict = model_to_dict(product)
            print("product_dict: ", product_dict)
            return {"code": 200, "msg": "found it!", "data": {"content": product_dict}}
        # return "developing..."


@app.route("/userdetail", methods=["GET"])
def UserDetailProvider():
    userName = request.args.get("username")
    user = Customers.query.filter_by(user_name=userName).first()
    if user is None:
        return {"code": 404, "msg": "no such user!"}
    else:
        user_dict = model_to_dict(user)
        print("user_dict: ", user_dict)
        return {"code": 200, "msg": "found it!", "data": {"content": user_dict}}


def model_to_dict(model_instance):
    result = {}
    for key, value in model_instance.__dict__.items():
        if not key.startswith('_') and key != 'metadata':
            result[key] = value
    return result


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
        print("no such file!")
        return send_file("product_Images/defaultimg.jpg", mimetype='image/jpeg')


@app.route('/upload/<filename>', methods=['GET'])
def get_image2(filename):
    print("uploading default image!")

    return send_file("product_Images/defaultimg.jpg", mimetype='image/jpeg')


@app.route("/purchase", methods=["GET"])
def UserPurchase():
    userName = request.args.get("username")
    product_id = request.args.get("product_id")
    buy_amount = int(request.args.get("buy_number"))
    print("product_id: ", product_id)
    product_to_update = Product.query.get(product_id)
    print("product_to_update: ", product_to_update)
    if product_to_update and userName is not None and userName != "":
        if product_to_update.inventory_amount <= buy_amount:
            return {"code": 404, "msg": "sold out!"}

        product_to_update.inventory_amount = product_to_update.inventory_amount - buy_amount
        product_to_update.sold_quantity = product_to_update.sold_quantity + buy_amount
        # product_to_update.sold_amount = product_to_update.sold_amount + product_to_update.price
        # db.session.commit()
    else:
        return {"code": 404, "msg": "product or user not found!"}

    customer = Customers.query.filter_by(user_name=userName).first()
    if customer is None:
        return {"code": 404, "msg": "User Not Found!"}
    customer_id = customer.customer_id
    print("customer_id: ", customer_id)
    salesperson_id = product_to_update.saleperson_id
    print("salesperson_id: ", salesperson_id)
    store_id = Salespersons.query.filter_by(salesperson_id=salesperson_id).first().store_id
    print("store_id: ", store_id)
    region_id = Store.query.filter_by(store_id=store_id).first().region_id
    print("region_id: ", region_id)
    if region_id is not None:
        targetRegion = Region.query.filter_by(region_id=region_id).first()
        print("targetRegion: ", targetRegion)
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
    return {"code": 200, "msg": "purchase success!"}


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
            return {"code": 200, "msg": "Region add success!"}

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
            return {"code": 200, "msg": "Salesperson add success!"}

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
            return {"code": 200, "msg": "Store add success!"}

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
            return {"code": 200, "msg": "Store add!"}
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
    page_index = request.args.get("page_index")
    print("page_index: ", page_index)
    page_size = request.args.get("page_size")
    print("page_size: ", page_size)
    products = Product.query
    columns = Product.__table__.columns.keys()
    if product_id is not None and product_id != "":
        products = products.filter_by(product_id=product_id)

    if product_name is not None and product_name != "":
        products = products.filter_by(product_name=product_name)
    products = products.all()
    print("products: ", products)

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
    salesperson_id = request.args.get("salesperson_id")
    transactions = Transactions.query
    columns = Transactions.__table__.columns.keys()
    if transaction_id is not None and transaction_id != "":
        transactions = transactions.filter_by(id=transaction_id)
    if store_id is not None and store_id != "":
        transactions = transactions.filter_by(store_id=store_id)
    if salesperson_id is not None and salesperson_id != "":
        transactions = transactions.filter_by(salesperson_id=salesperson_id)
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
    page_index = request.args.get("page_index")
    print("page_index: ", page_index)
    page_size = request.args.get("page_size")
    print("page_size: ", page_size)
    customers = Customers.query
    columns = Customers.__table__.columns.keys()
    if customer_id is not None and customer_id != "":
        customers = customers.filter_by(customer_id=customer_id)

    if user_name is not None and user_name != "":
        print("user_name: ", user_name)
        customers = customers.filter_by(user_name=user_name)

    if kind is not None and kind != "":
        customers = customers.filter_by(kind=kind)
    # startidx = (int(page_index) - 1) * int(page_size)
    customers = customers.all()
    # customers = customers.all()[startidx:startidx + int(page_size)]
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
        salespersons = salespersons.filter_by(salesperson_id=salesperson_id)
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
    # page_index = int(request.args.get("page_index"))
    # print("page_index: ", page_index)
    # page_size = int(request.args.get("page_size"))
    # print("page_size: ", page_size)
    products = Product.query
    columns = Product.__table__.columns.keys()
    if product_name is not None and product_name != "":
        products = products.filter(Product.product_name.ilike(f"%{product_name}%"))
        # print("products: ", products)
    products = products.all()
    print("content: ", products)
    # startidx = (page_index - 1) * page_size
    # print("startidx: ", startidx)
    # if startidx < len(products):
    #     if startidx + int(page_size) > len(products):
    #         products = products[startidx:]
    #     else:
    #         products = products[startidx:startidx + int(page_size)]
    # else:
    #     return {"code": 200, "msg": "success",
    #             "data": {"content": [], "totalElement": len([])}}/

    print("products: ", products)
    products_dict_list = [{column: getattr(product, column) for column in columns} for product in products]
    return {"code": 200, "msg": "success",
            "data": {"content": products_dict_list, "totalElement": len(products_dict_list)}}


@app.route("/editProduct", methods=["POST", "OPTIONS", "GET"])
def editProduct():
    if request.method == "GET":
        print("ADMIN is editing product!")
        return "developing..."
    elif request.method == "POST":
        print("ADMIN is posting product!")
        content = request.json
        print("content: ", content)
        productInfosDict = addItemTool.parseUpdateInfo(content)
        print("productInfos: ", productInfosDict)
        product_id = productInfosDict.get('product_id')
        print("product_id: ", product_id)
        product_to_update = Product.query.filter_by(product_id=product_id).first()
        print("product_to_update: ", product_to_update)
        if product_to_update:
            product_to_update.inventory_amount = productInfosDict.get('inventory_amount')
            product_to_update.price = productInfosDict.get('price')
            product_to_update.product_kind = productInfosDict.get('product_kind')
            product_to_update.product_description = productInfosDict.get('product_description')
            product_to_update.product_name = productInfosDict.get('product_name')
            product_to_update.saleperson_id = productInfosDict.get('saleperson_id')
            product_to_update.sold_quantity = productInfosDict.get('sold_quantity')
            db.session.commit()
            return {"code": 200, "msg": "update success!"}

        else:
            return {"code": 301, "msg": "update failed!"}

    else:
        return {"code": 301, "msg": "update failed!"}


@app.route("/editTransaction", methods=["POST", "OPTIONS", "GET"])
def editTransaction():
    if request.method == "GET":
        print("ADMIN is editing transaction!")
        return "developing..."
    elif request.method == "POST":
        print("ADMIN is posting transaction!")
        content = request.json
        print("content: ", content)
        transactionInfosDict = content
        print("transactionInfos: ", transactionInfosDict)
        transaction_id = transactionInfosDict.get('id')
        print("transaction_id: ", transaction_id)
        transaction_to_update = Transactions.query.filter_by(id=transaction_id).first()
        print("transaction_to_update: ", transaction_to_update)
        if transaction_to_update:
            transaction_to_update.customer_id = transactionInfosDict.get('customer_id')
            transaction_to_update.product_id = transactionInfosDict.get('product_id')
            transaction_to_update.store_id = transactionInfosDict.get('store_id')
            transaction_to_update.salesperson_id = transactionInfosDict.get('salesperson_id')
            transaction_to_update.order_number = transactionInfosDict.get('order_number')
            if transactionInfosDict.get('date') != 'Fri, 22 Jun 2001 00:00:00 GMT':
                date_object = datetime.fromisoformat(transactionInfosDict.get('date').replace('Z', '+00:00'))
                print("date_object: ", date_object, type(date_object))
            else:
                date_object = datetime.strptime(transactionInfosDict.get('date'), '%a, %d %b %Y %H:%M:%S %Z')
                print("date_object: ", date_object, type(date_object))
            transaction_to_update.date = date_object

            transaction_to_update.salesperson_name = transactionInfosDict.get('salesperson_name')
            transaction_to_update.product_number = int(transactionInfosDict.get('product_number'))
            db.session.commit()
            return {"code": 200, "msg": "update success!"}

        else:
            return {"code": 301, "msg": "update failed!"}

    else:
        return {"code": 301, "msg": "update failed!"}


@app.route("/editCustomer", methods=["POST", "OPTIONS", "GET"])
def editCustomer():
    if request.method == "GET":
        print("ADMIN is editing customer!")
        return "developing..."
    elif request.method == "POST":
        print("ADMIN is posting customer!")
        content = request.json
        print("content: ", content)
        customerInfosDict = content
        print(len(customerInfosDict))
        customer_id = customerInfosDict.get('customer_id')
        print("customer_id: ", customer_id)
        customer_to_update = Customers.query.filter_by(customer_id=customer_id).first()
        print("customer_to_update: ", customer_to_update)
        if customer_to_update:
            customer_to_update.age = customerInfosDict.get('age')
            customer_to_update.annual_income = customerInfosDict.get('annual_income')
            customer_to_update.business_category = customerInfosDict.get('business_category')
            customer_to_update.city = customerInfosDict.get('city')
            customer_to_update.customer_name = customerInfosDict.get('customer_name')
            # date_object = datetime.strptime(, '%a, %d %b %Y %H:%M:%S %Z')
            if customerInfosDict.get('birthday') is not None:
                date_object = datetime.strptime(customerInfosDict.get('birthday'), '%Y-%m-%dT%H:%M:%S.%f%z')
                customer_to_update.date_of_birth = date_object
            customer_to_update.email = customerInfosDict.get('email')
            customer_to_update.gender = customerInfosDict.get('gender')
            customer_to_update.income = customerInfosDict.get('income')
            customer_to_update.kind = customerInfosDict.get('kind')
            customer_to_update.marriage = customerInfosDict.get('marriage')
            # password = customerInfosDict.get('password')
            # if password is not None:
            #     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            #     customer_to_update.password = hashed_password
            customer_to_update.pet_kind = customerInfosDict.get('pet_kind')
            customer_to_update.phone_number = customerInfosDict.get('phone_number')
            customer_to_update.state = customerInfosDict.get('state')
            customer_to_update.street = customerInfosDict.get('street')
            customer_to_update.user_name = customerInfosDict.get('user_name')
            customer_to_update.zip_code = customerInfosDict.get('zip_code')
            db.session.commit()
        return {"code": 200, "msg": "update success!"}

    else:
        return {"code": 301, "msg": "update failed!"}


@app.route("/editSaleperson", methods=["POST", "OPTIONS", "GET"])
def editSaleperson():
    if request.method == "GET":
        print("ADMIN is editing saleperson!")
        return "developing..."
    elif request.method == "POST":
        print("ADMIN is posting saleperson!")
        salepersonInfosDict = request.json
        print("content: ", salepersonInfosDict)

        saleperson_id = salepersonInfosDict.get('salesperson_id')
        print("saleperson_id: ", saleperson_id)
        saleperson_to_update = Salespersons.query.filter_by(salesperson_id=saleperson_id).first()
        print("saleperson_to_update: ", saleperson_to_update)
        if saleperson_to_update:
            saleperson_to_update.city = salepersonInfosDict.get('city')
            saleperson_to_update.email = salepersonInfosDict.get('email')
            saleperson_to_update.job_title = salepersonInfosDict.get('job_title')
            saleperson_to_update.name = salepersonInfosDict.get('name')
            saleperson_to_update.phone = salepersonInfosDict.get('phone')
            saleperson_to_update.salary = salepersonInfosDict.get('salary')
            saleperson_to_update.state = salepersonInfosDict.get('state')
            saleperson_to_update.street = salepersonInfosDict.get('street')
            saleperson_to_update.store_id = salepersonInfosDict.get('store_id')
            saleperson_to_update.zipcode = salepersonInfosDict.get('zipcode')
            db.session.commit()
            return {"code": 200, "msg": "update success!"}

        else:
            return {"code": 301, "msg": "update failed!"}

    else:
        return {"code": 301, "msg": "update failed!"}


@app.route("/editStore", methods=["POST", "OPTIONS", "GET"])
def editStore():
    if request.method == "GET":
        print("ADMIN is editing store!")
        return "developing..."
    elif request.method == "POST":
        print("ADMIN is posting store!")
        storeInfosDict = request.json
        print("content: ", storeInfosDict)

        store_id = storeInfosDict.get('store_id')
        print("store_id: ", store_id)
        store_to_update = Store.query.filter_by(store_id=store_id).first()
        print("store_to_update: ", store_to_update)
        if store_to_update:
            store_to_update.city = storeInfosDict.get('city')
            store_to_update.manager = storeInfosDict.get('manager')
            store_to_update.number_of_salesperson = storeInfosDict.get('number_of_salesperson')
            store_to_update.region_id = storeInfosDict.get('region_id')
            store_to_update.state = storeInfosDict.get('state')
            store_to_update.street = storeInfosDict.get('street')
            store_to_update.zip_code = storeInfosDict.get('zip_code')
            db.session.commit()
            return {"code": 200, "msg": "update success!"}

        else:
            return {"code": 301, "msg": "update failed!"}

    else:
        return {"code": 301, "msg": "update failed!"}


@app.route("/editRegion", methods=["POST", "OPTIONS", "GET"])
def editRegion():
    if request.method == "GET":
        print("ADMIN is editing region!")
        return "developing..."
    elif request.method == "POST":
        print("ADMIN is posting region!")
        regionInfosDict = request.json
        print("content: ", regionInfosDict)

        region_id = regionInfosDict.get('region_id')
        print("region_id: ", region_id)
        region_to_update = Region.query.filter_by(region_id=region_id).first()
        print("region_to_update: ", region_to_update)
        if region_to_update:
            region_to_update.region_id = regionInfosDict.get('region_id')
            region_to_update.region_manager = regionInfosDict.get('region_manager')
            region_to_update.region_name = regionInfosDict.get('region_name')
            region_to_update.sold_amount = regionInfosDict.get('sold_amount')
            region_to_update.sold_quantity = regionInfosDict.get('sold_quantity')
            region_to_update.store_number = regionInfosDict.get('store_number')
            db.session.commit()
            return {"code": 200, "msg": "update success!"}

        else:
            return {"code": 301, "msg": "update failed!"}

    else:
        return {"code": 301, "msg": "update failed!"}


@app.route("/delRegion", methods=["POST", "OPTIONS", "GET"])
def delRegion():
    if request.method == "GET":
        print("ADMIN is deleting region!")
        region_id = request.args.get("region_id")
        print("region_id: ", region_id)
        region_to_delete = Region.query.filter_by(region_id=region_id).first()
        print("region_to_delete: ", region_to_delete)
        if region_to_delete:
            db.session.delete(region_to_delete)
            storesInRegion = Store.query.filter_by(region_id=region_id).all()
            for store in storesInRegion:
                db.session.delete(store)
            db.session.commit()
            return {"code": 200, "msg": "delete success!"}
        else:
            return {"code": 301, "msg": "delete failed!"}
    else:
        return "this is an option request!..."


@app.route("/delProduct", methods=["POST", "OPTIONS", "GET"])
def deleteProduct():
    if request.method == "GET":
        print("ADMIN is deleting product!")
        product_id = request.args.get("product_id")
        print("product_id: ", product_id)
        product_to_delete = Product.query.filter_by(product_id=product_id).first()
        print("product_to_delete: ", product_to_delete)
        if product_to_delete:
            db.session.delete(product_to_delete)
            db.session.commit()
            return {"code": 200, "msg": "delete success!"}
        else:
            return {"code": 301, "msg": "delete failed!"}
    else:
        return "developing!..."


@app.route("/delTransaction", methods=["POST", "OPTIONS", "GET"])
def deletetrans():
    if request.method == "GET":
        print("ADMIN is deleting transaction!")
        transaction_id = request.args.get("id")
        print("transaction_id: ", transaction_id)
        transaction_to_delete = Transactions.query.filter_by(id=transaction_id).first()
        print("transaction_to_delete: ", transaction_to_delete)
        if transaction_to_delete:
            db.session.delete(transaction_to_delete)
            db.session.commit()
            return {"code": 200, "msg": "delete success!"}
        else:
            return {"code": 301, "msg": "delete failed!"}
    else:
        return "developing!..."


@app.route("/delCustomer", methods=["POST", "OPTIONS", "GET"])
def delcustomer():
    if request.method == "GET":
        print("ADMIN is deleting customer!")
        customer_id = request.args.get("customer_id")
        print("customer_id: ", customer_id)
        customer_to_delete = Customers.query.filter_by(customer_id=customer_id).first()
        print("customer_to_delete: ", customer_to_delete)
        if customer_to_delete:
            db.session.delete(customer_to_delete)
            db.session.commit()
            return {"code": 200, "msg": "delete success!"}
        else:
            return {"code": 301, "msg": "delete failed!"}
    else:
        return "developing!..."


@app.route("/delSaleperson", methods=["POST", "OPTIONS", "GET"])
def delsaleperson():
    if request.method == "GET":
        print("ADMIN is deleting saleperson!")
        saleperson_id = request.args.get("salesperson_id")
        print("saleperson_id: ", saleperson_id)
        saleperson_to_delete = Salespersons.query.filter_by(salesperson_id=saleperson_id).first()
        print("saleperson_to_delete: ", saleperson_to_delete)
        if saleperson_to_delete:
            db.session.delete(saleperson_to_delete)
            db.session.commit()
            return {"code": 200, "msg": "delete success!"}
        else:
            return {"code": 301, "msg": "delete failed!"}
    else:
        return "this is an option request!..."


@app.route("/delStore", methods=["POST", "OPTIONS", "GET"])
def delstore():
    if request.method == "GET":
        print("ADMIN is deleting store!")
        store_id = request.args.get("store_id")
        print("store_id: ", store_id)
        store_to_delete = Store.query.filter_by(store_id=store_id).first()
        print("store_to_delete: ", store_to_delete)
        if store_to_delete:
            db.session.delete(store_to_delete)
            db.session.commit()
            return {"code": 200, "msg": "delete success!"}
        else:
            return {"code": 301, "msg": "delete failed!"}
    else:
        return "this is an option request!..."


@app.route("/sortproduct", methods=["POST", "OPTIONS", "GET"])
def productSorter():
    print("sorting product!")
    if request.method == "GET":
        cateria = request.args.get("by")
        print("cateria: ", cateria)
        columns = Product.__table__.columns.keys()
        if cateria == "price":
            products = Product.query.order_by(Product.price.desc()).all()
            products_dict_list = [{column: getattr(product, column) for column in columns} for product in products]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": products_dict_list, "totalElement": len(products_dict_list)}}
        elif cateria == "sold_quantity":
            products = Product.query.order_by(Product.sold_quantity.desc()).all()
            products_dict_list = [{column: getattr(product, column) for column in columns} for product in products]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": products_dict_list, "totalElement": len(products_dict_list)}}
        elif cateria == "inventory_amount":
            products = Product.query.order_by(Product.inventory_amount.desc()).all()
            products_dict_list = [{column: getattr(product, column) for column in columns} for product in products]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": products_dict_list, "totalElement": len(products_dict_list)}}
        elif cateria == "sold_amount":
            products = Product.query.order_by(Product.sold_amount.desc()).all()
            products_dict_list = [{column: getattr(product, column) for column in columns} for product in products]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": products_dict_list, "totalElement": len(products_dict_list)}}
        else:
            return {"code": 301, "msg": "sort failed!"}

    else:
        return "this is an option request!..."


@app.route("/sortsaleperson", methods=["POST", "OPTIONS", "GET"])
def salepersonSorter():
    if request.method == "GET":
        cateria = request.args.get("by")
        print("cateria: ", cateria)
        columns = Salespersons.__table__.columns.keys()
        if cateria == "salary":
            salespersons = Salespersons.query.order_by(Salespersons.salary.desc()).all()
            salespersons_dict_list = [{column: getattr(salesperson, column) for column in columns} for salesperson in
                                      salespersons]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": salespersons_dict_list, "totalElement": len(salespersons_dict_list)}}
        else:
            return {"code": 301, "msg": "sort failed!"}

    else:
        return "this is an option request!..."


@app.route("/sortregion", methods=["POST", "OPTIONS", "GET"])
def regionSorter():
    if request.method == "GET":
        cateria = request.args.get("by")
        print("cateria: ", cateria)
        columns = Region.__table__.columns.keys()
        if cateria == "sold_amount":
            regions = Region.query.order_by(Region.sold_amount.desc()).all()
            regions_dict_list = [{column: getattr(region, column) for column in columns} for region in regions]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": regions_dict_list, "totalElement": len(regions_dict_list)}}
        elif cateria == "sold_quantity":
            regions = Region.query.order_by(Region.sold_quantity.desc()).all()
            regions_dict_list = [{column: getattr(region, column) for column in columns} for region in regions]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": regions_dict_list, "totalElement": len(regions_dict_list)}}
        elif cateria == "store_number":
            regions = Region.query.order_by(Region.store_number.desc()).all()
            regions_dict_list = [{column: getattr(region, column) for column in columns} for region in regions]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": regions_dict_list, "totalElement": len(regions_dict_list)}}
        else:
            return {"code": 301, "msg": "sort failed!"}


@app.route("/sortstore", methods=["POST", "OPTIONS", "GET"])
def storeSorter():
    if request.method == "GET":
        cateria = request.args.get("by")
        print("cateria: ", cateria)
        columns = Store.__table__.columns.keys()
        if cateria == "number_of_salespersons":
            stores = Store.query.order_by(Store.number_of_salespersons.desc()).all()
            stores_dict_list = [{column: getattr(store, column) for column in columns} for store in stores]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": stores_dict_list, "totalElement": len(stores_dict_list)}}
        else:
            return {"code": 301, "msg": "sort failed!"}


@app.route("/sortcustomer", methods=["POST", "OPTIONS", "GET"])
def customerSorter():
    if request.method == "GET":
        cateria = request.args.get("by")
        print("cateria: ", cateria)
        columns = Customers.__table__.columns.keys()
        if cateria == "income":
            customers = Customers.query.order_by(Customers.income.desc()).all()
            customers_dict_list = [{column: getattr(customer, column) for column in columns} for customer in customers]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": customers_dict_list, "totalElement": len(customers_dict_list)}}
        elif cateria == "annual_income":
            customers = Customers.query.order_by(Customers.annual_income.desc()).all()
            customers_dict_list = [{column: getattr(customer, column) for column in columns} for customer in customers]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": customers_dict_list, "totalElement": len(customers_dict_list)}}
        elif cateria == "age":
            customers = Customers.query.order_by(Customers.age.desc()).all()
            customers_dict_list = [{column: getattr(customer, column) for column in columns} for customer in customers]
            return {"code": 200, "msg": "sort success!",
                    "data": {"content": customers_dict_list, "totalElement": len(customers_dict_list)}}
        else:
            return {"code": 301, "msg": "sort failed!"}


@app.route("/editUser", methods=["POST", "OPTIONS", "GET"])
def updateUserInfo():
    if request.method == "POST":
        print("USER is editing user!")
        customerInfosDict = request.json
        print("content: ", customerInfosDict)
        print("TargetUser: ", len(customerInfosDict))

        customer_id = customerInfosDict.get('customer_id')
        print("customer_id: ", customer_id)
        TargetUser = Customers.query.filter_by(customer_id=customer_id).first()
        print("TargetUser: ", TargetUser)
        if TargetUser:
            TargetUser.age = customerInfosDict.get('age')
            TargetUser.annual_income = customerInfosDict.get('annual_income')
            TargetUser.business_category = customerInfosDict.get('business_category')
            TargetUser.city = customerInfosDict.get('city')
            TargetUser.state = customerInfosDict.get('state')
            TargetUser.street = customerInfosDict.get('street')
            TargetUser.zip_code = customerInfosDict.get('zip_code')
            TargetUser.marriage = customerInfosDict.get('marriage')
            TargetUser.pet_kind = customerInfosDict.get('pet_kind')
            TargetUser.kind = customerInfosDict.get('kind')
            TargetUser.income = customerInfosDict.get('income')
            TargetUser.customer_name = customerInfosDict.get('customer_name')
            TargetUser.user_name = customerInfosDict.get('user_name')
            TargetUser.email = customerInfosDict.get('email')
            TargetUser.phone_number = customerInfosDict.get('phone_number')
            TargetUser.gender = customerInfosDict.get('gender')
            date_format = "%m/%d/%Y"
            date_object = datetime.strptime(customerInfosDict.get('date_of_birth'), date_format)
            TargetUser.date_of_birth = date_object
            db.session.commit()
            return {"code": 200, "msg": "update success!"}
        else:
            return {"code": 301, "msg": "update failed!"}

    else:
        return "this is not post request!..."


@app.route("/groupCutomerByGender", methods=["POST", "OPTIONS", "GET"])
def CustomerGroupByGender():
    if request.method == "GET":
        query = (
            Customers.query.with_entities(func.count(Customers.customer_id), Customers.gender)
            .group_by(Customers.gender)
            .order_by(func.count(Customers.customer_id).desc())
        )
        result = query.all()
        result = [{"count": count, "gender": gender} for count, gender in result]

        print(result)
        return {"code": 200, "msg": "success",
                "data": {"content": result, "totalElement": len(result)}}


@app.errorhandler(Exception)
def handle_500_error(e):
    print("error :", e)
    resp = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    # set 'debug = true' allows to restart application when saving a file
    app.run(host='0.0.0.0', port=8080, debug=True)
