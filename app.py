from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basePath = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basePath, 'templates')

# need to specify the template directory if it is not in the base directory
app = Flask(__name__, template_folder=template_dir)
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
    from models import User

    db.create_all()  # create all the table that haven't been created
