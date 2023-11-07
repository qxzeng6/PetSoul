from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

basePath = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basePath, 'templates')

# need to specify the template directory if it is not in the base directory
app = Flask(__name__, template_folder=template_dir)
CORS(app)
db = SQLAlchemy()
app.config.from_object('config')
# load config information, including SQLALCHEMY_DATABASE_URI
# SQLALCHEMY_DATABASE_URI = "database+drive://username:password@localhost:port/datbase?other configs"
#                    example:mysql+pymysql://root:@127.0.0.1:3306/db

# config that commit every changes automatically
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_TRACK_MODIFICATIONS = False
with app.app_context():
    db.init_app(app)  # init db in app

    # import all the models you want to use before create_all function
    from models.User import User
    from models.Product import Product
    from models.Customers import Customers
    from models.Transactions import Transactions
    from models.Salespersons import Salespersons
    from models.Store import Store
    from models.Region import Region

    db.create_all()  # create all the table that haven't been created
