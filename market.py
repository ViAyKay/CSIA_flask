from enum import unique
from pydoc import synopsis
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://computer:spark@localhost/library_sys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.BLOB, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)

class Users (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.string(100), nullable=False, unique=True)
    email = db.Column(db.string(200), nullable=False, unique=True)
    superuser = db.Column(db.Boolean, nullable=False)

class Borrow (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.utcnow)
    book_id = db.Column(db.Integer, ForeignKey(Book.id))
    user_id = db.Column(db.Integer, ForeignKey(Book.id))
    return_date = db.Column(db.Date, nullable=False) 



@app.route('/')
def home_page():
    return render_template('loginpage.html') 

