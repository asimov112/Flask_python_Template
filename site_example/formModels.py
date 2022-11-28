from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,IntegerRangeField
from wtforms.validators import DataRequired,Length,EqualTo,email

class loginAuthentication(FlaskForm):
    emailAddress = StringField("Email address",validators=[DataRequired(),Length(min=10,max=50)])
    password = PasswordField("password",validators=[DataRequired(),Length(min=8,max=50)])
    submission = SubmitField("login")

class subscribeForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    emailAddress = StringField('Email',validators=[Length(min=6),email(message="Please enter a valid email"),DataRequired()])
    password = PasswordField('password',validators=[DataRequired(),Length(min=8,message="Please enter a password greater than 8 characters")])
    passwordConfirmation = PasswordField('Confirm password',validators=[DataRequired(),EqualTo(fieldname='password')])
    submission = SubmitField("Register")

class adminAccountCreation(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    emailAddress = StringField("Email",validators=[Length(min=6),email(message="Please enter a valid email"),DataRequired()])
    password = PasswordField("password",validators=[DataRequired(),Length(min=8,message="Please enter a password greater than 6 characters")])
    passwordConfirmation = PasswordField("Confirm password",validators=[DataRequired(),EqualTo(fieldname='password')])
    submission = SubmitField("Register")

class adminAuthorisation(FlaskForm):
    code = StringField("Authorisation code",validators=[DataRequired(),Length(min=6)])
    submission = SubmitField("submit")

class userSettings(FlaskForm):
    password = PasswordField("password",validators=[DataRequired(),Length(min=8,message="Please enter a password greater than 8 characters")])
    passwordConfirmation = PasswordField("Confirm password",validators=[DataRequired(),EqualTo(fieldname='password')])
    submission = SubmitField("submit")

class basketAddition(FlaskForm):
    quantity = StringField("quantity",validators=[DataRequired(),Length(min=1,message="Please supply at least one to add to basket please")])
    submission = SubmitField("Add to cart")

class reviewingItem(FlaskForm):
    reviewInformation = TextAreaField("review",validators=[DataRequired(),Length(min=20,message="Please insert a minimum of a sentence about this product")])
    starRating = StringField("starRating",validators=[DataRequired(),Length(min=1,max=1)])
    submission = SubmitField("Add review")