from site_example.formModels import *
from werkzeug.security import check_password_hash
from site_example.models import User, Admin, Product, Review
from site_example import app, database, login_manager
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import *
import pytest
import datetime
import re

@pytest.mark.fixture
def app_ctx(app):
    with app.app_context():
        yield

@login_manager.user_loader
def load_user(userId):
    return User.query.get(userId)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
@pytest.mark.usefixtures("app_ctx")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    sqlsyntax = "'(''|[^'])*'"
    sqlReservedWords = "\b(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})\b"

    form = loginAuthentication()
    if form.validate_on_submit():

        if re.match(sqlsyntax,form.emailAddress.data) or re.match(sqlReservedWords,form.emailAddress.data):
            app.logger.info("Warning SQL injection detected")
            return redirect(url_for("login"))
        if re.match(sqlsyntax,form.password.data) or re.match(sqlReservedWords,form.password.data):
            app.logger.info("Warning SQL injection detected")
            return redirect(url_for("login"))

        user = User.query.get(form.emailAddress.data)
        admin = Admin.query.get(form.emailAddress.data)
        if user:
            if check_password_hash(user.password,form.password.data):
                user.authenticated = True
                database.session.add(user)
                database.session.commit()
                login_user(user,remember=True)
                flash("Logged in")
                return redirect(url_for("index"))
        elif admin:
            if check_password_hash(admin.password,form.password.data):
                admin.authenticated = True
                database.session.add(admin)
                database.session.commit()
                login_user(admin,remember=True)
                flash("Logged in")
                return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect email or password")
            error = "No user exists by this name"
            return render_template("login.jinja2",form=form,loginFail = error)
    return render_template("login.jinja2",form=form)

@app.route("/user/create_account",methods=["GET","POST"])
@pytest.mark.usefixtures("app_ctx")
def signUp():
    form = subscribeForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.emailAddress.data).first()
        if existing_user is None:
            newUser = User(name=form.name.data,email=form.emailAddress.data)
            newUser.secure_password(form.password.data)
            database.session.add(newUser)
            database.session.commit()
            flash("Successfully created account")
            return redirect(url_for("login"))
        else:
            return flash("user already exists")
    else:
        return render_template("signup.jinja2",form=form)

@app.route("/admin",methods=["GET","POST"])
@pytest.mark.usefixtures("app_ctx")
def adminAccount():
    form = adminAuthorisation()
    if form.validate_on_submit():
        if form.code.data == "006780":
            formAuth = adminAccountCreation()
            if formAuth.validate_on_submit():
                existing_admin = Admin.query.filter_by(emailAddress=formAuth.name.data).first()
                if existing_admin is None:
                    newAdmin = Admin(name=formAuth.name.data,email=formAuth.emailAddress.data)
                    newAdmin.secure_password(formAuth.password.data)
                    newAdmin.secure_password(formAuth.passwordConfirmation.data)
                    database.session.add(newAdmin)
                    database.session.commit()
                    flash("Successfully created administration account")
                    return redirect(url_for("admin_login"))
                else:
                    flash("Admin account already exists")
            else:
                return render_template("admin_account_create.jinja2",form=formAuth)
        else:
            return render_template("admin_authorisation.jinja2",form=form)
    else:
        return render_template("admin_authorisation.jinja2",form=form)

@app.route("/products",methods=["GET","POST"])
@pytest.mark.usefixtures("app_ctx")
def products():
    selectedItem = request.args.get("item")
    if selectedItem:

        itemInstance = Product.query.get(selectedItem)
        review = Review.query.filter_by(productId=itemInstance.id).limit(10).all()

        form = basketAddition()

        if form.validate_on_submit():
            cart = session.get("basket",{})
            cart[selectedItem] = form.quantity.data
            session["basket"] = cart
        else:
            return render_template("product.jinja2",form=form,item=itemInstance,itemReview=review)
            
    productSelection = Product.query.all()
    return render_template("products.html",products=productSelection)


@app.route("/basket",methods=["GET","POST"])
@pytest.mark.usefixtures("app_ctx")
@login_required
def basketItems():
    basket = []
    basketSession = session.get("basket",None)
    if basketSession:
        for key in basketSession:
            item = Product.query.filter(Product.id == key).first()
            quantity = int(basketSession[key])
            price = item.price * quantity
            totalPrice = price
            basket.append([item.productName,quantity,price])
    else:
        flash("No items currently in basket")
        return redirect(url_for("index"))
    return render_template("basket.html",cart=basket, total=totalPrice)


@app.route("/basket/payment",methods=["GET","POST"])
@login_required
def finalPayment():
    return redirect(url_for("index"))

@app.route("/user/settings",methods=["GET","POST"])
@pytest.mark.usefixtures("app_ctx")
@login_required
def settings():
    if current_user.is_authenticated():
        userLoggedIn = User.query.get(current_user.get_id())
        userInformation = [userLoggedIn.name,userLoggedIn.email,userLoggedIn.created]
        sqlsyntax = "'(''|[^'])*'"
        sqlReservedWords = "\b(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})\b"
        form = userSettings()
        if form.validate_on_submit():
            if re.match(sqlsyntax,form.password.data) or re.match(sqlReservedWords,form.password.data):
                app.logger.info("Warning SQL injection detected")
                return redirect(url_for("settings"))
            userLoggedIn.password = form.password.data
            database.session.commit()
        return render_template("settings.jinja2",form=form,user = userInformation)
    else:
        return redirect(url_for("index"))

@app.route("/review/<productId>",methods=["GET","POST"])
@pytest.mark.usefixtures("app_ctx")
@login_required
def reviewItem(productId):
    if current_user.is_authenticated:
        sqlsyntax = "'(''|[^'])*'"
        sqlReservedWords = "\b(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})\b"

        if re.match(sqlsyntax,productId) or re.match(sqlReservedWords,productId):
            app.logger.info("Warning SQL injection detected")
            return redirect("products")

        form = reviewingItem()
        product = Product.query.get(productId)
        userAccount = User.query.get(current_user.get_id())
        if form.validate_on_submit():
            newReview = Review(useremail=userAccount.email,
                                productid=product.id,
                                review=form.reviewInformation.data,
                                starRating=form.starRating.data,
                                date=datetime.datetime.now())
            database.session.add(newReview)
            database.session.commit()
            return redirect(url_for("products"))
        else:
            return render_template("itemReview.jinja2",form=form)
    else:
        app.logger.info("Warning unauthorised user is attempting to make a review")

@app.route("/logout")
@pytest.mark.usefixtures("app_ctx")
@login_required
def logout():
    user = current_user
    user.authenticated = False
    database.session.add(user)
    database.session.commit()
    logout_user()
    flash("Logged out")
    return render_template("index.html")

