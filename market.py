from enum import unique
from pydoc import synopsis
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://computer:spark@localhost/library_sys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "whatgoesupmustneverstayupforthedevillooksforanomalousbasterds101"

#Create a form class
class LoginForm(FlaskForm):
    name = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class Book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.BLOB, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)

class Librarian (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    superuser = db.Column(db.Boolean, nullable=False)

class Borrow (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #date = db.Column(db.Date, default=date.utcnow)
    book_id = db.Column(db.Integer, ForeignKey(Book.id))
    return_date = db.Column(db.Date, nullable=False) 



@app.route('/', methods=['GET', 'POST'])
def login_page():
    name = None
    password = None
    form = LoginForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        form.name.data = ''
        form.password.data =''

    return render_template('loginpage.html', name = name, password = password, form = form) 





