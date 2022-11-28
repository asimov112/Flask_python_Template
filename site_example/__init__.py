from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask import g
from sqlite3 import *

login_manager = LoginManager()

app = Flask(__name__,template_folder="templates")

UPLOAD_FOLDER = "uploads"

app.config.update(
    SECRET_KEY= "00XBAstGeDPlIwaSDFgtA14128",
    SESSION_COOKIE_SAMESITE="Strict",
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user.sqlite3'
)

database = SQLAlchemy(app)
login_manager.init_app(app)
database.init_app(app)

import site_example.models

with app.app_context():
    database.create_all()
    if not site_example.models.Product.query.all():
        productsInsert = [
                            site_example.models.Product(1,"Brain Reaction",4.99,100,"/uploads/"),
                            site_example.models.Product(2,"Voodoo Child",3.99,100,"/uploads/"),
                            site_example.models.Product(3,"El Capitan",2.99,100,"/uploads/"),
                            site_example.models.Product(4,"No woman no cry",5.99,100,"/uploads/")
                        ]
        database.session.add_all(productsInsert)
        database.session.commit()

from .views import *