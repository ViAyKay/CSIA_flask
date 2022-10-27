from enum import unique
from pydoc import synopsis
from django.shortcuts import redirect, render
from flask import Flask, render_template, url_for, flash, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_migrate import Migrate

from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://computer:spark@localhost/library_sys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "whatgoesupmustneverstayupforthedevillooksforanomalousbasterds101"

#Flask_Login Stuff
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.BLOB, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)

class  Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #password = db.Column(db.String(100), nullable=False, unique=True)
    superuser = db.Column(db.Boolean, nullable=False)
    #password_stuff
    password = db.Column(db.String(128))
    #password_hash = db.Column(db.String(128))


    @property
    def password(self):
      raise AttributeError('password is unreadable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Borrow (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #date = db.Column(db.Date, default=date.utcnow)
    book_id = db.Column(db.Integer, ForeignKey(Book.id))
    return_date = db.Column(db.Date, nullable=False) 

#One time use form to create account for librarian DELETE THIS AFTER CREATING THE ACCOUNT
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a form class
class LoginForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

@app.route('/', methods=['GET', 'POST'])
def login_page():
    name = None
    password = None
    form = LoginForm()
    #Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for(libview))
            else:
                flash("incorrect credentials")

       

    return render_template('loginpage.html', name = name, password = password, form = form) 

@app.route('/libview', methods=['GET', 'POST'])
@login_required
def libview():
    return render_template('libview.html')

@app.route('/u', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        if user is None:
            user = Users(name=form.name.data,superuser = True, password=form.password.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.password.data = ''
    
    #our_users = Users.query.order_by(Users.date_added)
    return render_template ( "onetimeuseradd.html", form=form, name=name)#our_users=our_users)



    
    




