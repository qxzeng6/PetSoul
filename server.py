# import package
import bcrypt
from app import app, db
from models.User import User
from flask import Flask, render_template, request
import os

# # create Flask object as the application
# app = Flask(__name__)


# mapping the route to a python function


@app.route("/")
def welcomeGuest():
    # Drop a homepage in the templates called index.html, currently has no this html file
    return render_template("index.html")



@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form.get('username')
        password = request.form.get('password')
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        user = User(name, hashed_password)
        db.session.add(user)
        db.session.commit()
        return welcomeGuest(name)


if __name__ == "__main__":
    # set 'debug = true' allows to restart application when saving a file
    # check this in localhost:8080 you will understand
    app.run(host='0.0.0.0', port=8080, debug=True)
