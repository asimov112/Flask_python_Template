from site_example import database
from werkzeug.security import generate_password_hash
import datetime

class User(database.Model):
    __tablename__ = "user"
    name = database.Column(database.String,nullable=False)
    email = database.Column(database.String,primary_key=True)
    password = database.Column(database.String,nullable=False)
    authenticated = database.Column(database.Boolean,default=False,nullable=False)
    created = database.Column(database.DateTime,nullable=False,default=datetime.datetime.now)
    last_accessed = database.Column(database.DateTime,nullable=True)

    def __init__(self,name,email,Authenticated=True):
        self.name = name
        self.email = email
        self.authenticated = Authenticated
        self.created = datetime.datetime.now()
        self.last_accessed = datetime.datetime.now()

    def is_active(self):
        return True
    def get_id(self):
        return self.email
    def is_authenticated(self):
        return self.authenticated
    def is_anonymous(self):
        return False

    def secure_password(self,password):
        self.password = generate_password_hash(password,method="sha256")

class Admin(database.Model):
    __tablename__ = "admin"
    name = database.Column(database.String,nullable=False)
    email = database.Column(database.String,primary_key=True)
    password = database.Column(database.String,nullable=False)
    authenticated = database.Column(database.Boolean,default=False,nullable=False)
    created = database.Column(database.DateTime,nullable=False,default=datetime.datetime.now)
    last_accessed = database.Column(database.DateTime,nullable=True)

    def __init__(self,name,email,Authenticated=True):
        self.name = name
        self.email = email
        self.authenticated = Authenticated
        self.created = datetime.datetime.now()
        self.last_accessed = datetime.datetime.now()

    def is_active(self):
        return True
    def get_id(self):
        return self.email
    def is_authenticated(self):
        return self.authenticated
    def is_anonymous(self):
        return False

    def secure_password(self,password):
        self.password = generate_password_hash(password,method="sha256")

class Product(database.Model):
    __tablename__ = "product"

    id = database.Column(database.Integer,primary_key=True)
    productName = database.Column(database.String,nullable=False)
    price = database.Column(database.Float,nullable=False)
    quantity = database.Column(database.Integer,nullable=False)
    image = database.Column(database.String,nullable=True)

    def __init__(self,id,productName,price,quantity,image):
        self.id = id
        self.productName = productName
        self.price = price
        self.quantity = quantity
        self.image = image

class Review(database.Model):
    __tablename__ = "review"
    id = database.Column(database.Integer,primary_key=True)
    userEmail = database.Column(database.String,nullable=False)
    productId = database.Column(database.Integer,nullable=False)
    review = database.Column(database.String,nullable=True)
    starRating = database.Column(database.Integer,nullable=False)
    date = database.Column(database.DateTime,nullable=False)

    def __init__(self,useremail,productid,review,starRating,date):
        self.userEmail = useremail
        self.productId = productid
        self.review = review
        self.starRating = starRating
        self.date = date