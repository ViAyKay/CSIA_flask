from pydoc import synopsis
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/')
def home_page():
    return render_template('loginpage.html') 

