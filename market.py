from enum import unique
from pydoc import synopsis
from flask import Flask, request, render_template, url_for, flash,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, EmailField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
import os
from flask_migrate import Migrate
import uuid as uuid
from sqlalchemy import func, select
from sqlalchemy import ForeignKey
from flask import Flask, session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dangerzone@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "whatgoesupmustneverstayupforthedevillooksforanomalousbasterds101"


def first_highest_book_id_record():
    result = db.session.query(func.max(Book.id)).scalar()
    return result

def first_highest_user_id_record():
    result = db.session.query(func.max(Users.id)).scalar()
    return result



class Borrower (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    apartment_number = db.Column(db.String(255), nullable = False)
    late_returns = db.Column(db.Integer, nullable = False, default=0)

class Book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.BLOB, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)

class  Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    superuser = db.Column(db.Boolean, nullable=False)
    password_hash = db.Column(db.String(128))


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
    borrow_date = db.Column(db.Date, default=date.today())
    book_id = db.Column(db.Integer, ForeignKey(Book.id))
    borrower_id = db.Column (db.Integer, ForeignKey(Borrower.id))
    overdue = db.Column(db.Boolean, nullable = False, default=False)
    daysleft = db.Column(db.Integer, nullable = False, default=7)
    return_date = db.Column(db.Date, nullable=False) 
    
class BorrowForm(FlaskForm):
    book_id = IntegerField("book id", validators=[DataRequired(), NumberRange(min=1, max=100)])
    borrower_id = IntegerField("borrower field", validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField("Submit")

class BorrowerForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()], widget=TextArea())
    apartment_number = StringField("Apartment Number", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    synopsis = StringField("Synopsis", validators=[DataRequired()], widget=TextArea())
    available = BooleanField("Availability", validators=[DataRequired()])
    submit = SubmitField("Submit")

#One time use form to create account for librarian DELETE THIS AFTER CREATING THE ACCOUNT
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/borrowadd', methods=['GET','POST'])
def borrowadd():
    form = BorrowForm()

    max_book_id = first_highest_book_id_record()
    max_borrower_id = first_highest_user_id_record()

    if form.validate_on_submit():
        if form.book_id.data < max_book_id and form.borrower_id < max_borrower_id:
            borrow = Borrow(book_id=form.book_id.data, borrower_id=form.borrower_id.data, return_date= date.today() + timedelta(days=20) )
            #Clear the form
            form.book_id.data = ''
            form.borrower_id.data = '' 
        
            db.session.add(borrow)
            db.session.commit() 
            flash("Borrow added to database successfully")

        else:
            flash("Please enter valid IDs")

    return render_template("borrowadd.html", form=form)

@app.route('/borrowview', methods=['GET','POST'])
@login_required
def borrowview():   
    #Grab all books from database
    borrows = Borrow.query.order_by(Borrow.id)
    return render_template('borrowview.html', borrows = borrows)
    
   


@app.context_processor
def base():
    form = SearchForm() 
    return dict(form=form)

@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    books = Book.query
    if form.validate_on_submit():
        
        booklook.searched = form.searched.data

        books = books.filter(Book.title.like('%' + booklook.searched + '%'))
        books = books.order_by(Book.title).all()

        return render_template("search.html", form=form, searched = booklook.searched, books = books)

@app.route('/pplsearch', methods=["POST"])
def borrowersearch():
    form = SearchForm()
    borrowers = Borrower.query
    if form.validate_on_submit():

            brwrlook.searched = form.searched.data
            borrowers = borrowers.filter(Borrower.first_name.like('%' + brwrlook.searched + '%'))
            borrowers = borrowers.order_by(Borrower.first_name).all()

            return render_template("pplsearch.html", form=form, searched = brwrlook.searched, borrowers = borrowers)


@app.route('/u', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    #Hashing Password
    
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data,superuser = True, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.password_hash.data = ''
    
    #our_users = Users.query.order_by(Users.date_added)
    return render_template ( "onetimeuseradd.html", form=form, name=name)#our_users=our_users)

#Create a form class
class LoginForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        if user:
            #check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('libview'))
            else:
                flash("WRONG PASSWORD TRY AGAIN") 
        else:
            flash("USER DOES NOT EXIST")

    return render_template('loginpage.html', form=form)



@app.route('/globbedygoo', methods=['GET', 'POST'])
def hello_world():
    form = BorrowerForm()

    if form.validate_on_submit():
        borrower = Borrower(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, apartment_number=form.apartment_number.data)
        #Clear the form
        form.first_name.data = ''
        form.last_name.data = ''
        form.email.data = ''
        form.apartment_number.data = ''

        #Add borrower data to database
        db.session.add(borrower)
        db.session.commit()

        flash("Borrower added to database successfully")

    return render_template("borroweradd.html", form=form)

@app.route('/brwrview/edit/<int:id>', methods=['GET', 'POST'])
def edit_borrower(id):
    borrower = Borrower.query.get_or_404(id)
    form = BorrowerForm()
    if form.validate_on_submit():
        borrower.first_name = form.first_name.data
        borrower.last_name = form.last_name.data
        borrower.email = form.email.data
        borrower.apartment_number = form.apartment_number.data

        db.session.add(borrower)
        db.session.commit()
        flash("Book information has been updated")
        return redirect(url_for('brwrview'))
    form.first_name.data = borrower.first_name
    form.last_name.data = borrower.last_name
    form.email.data = borrower.email
    form.apartment_number.data = borrower.apartment_number
    return render_template('edit_borrower.html', form=form)

@app.route('/brwrview', methods=['GET', 'POST'])
@login_required
def brwrview():
    #Grab all books from database
    borrowers = Borrower.query.order_by(Borrower.id)
    return render_template('brwrview.html', borrowers = borrowers)

@app.route('/brwrview/<int:id>', methods=['GET', 'POST'])
@login_required
def brwrlook():
    borrower = Borrower.query.get_or_404(id)

@app.route('/brwrview/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def brwrdelete(id):
    borrower_to_delete = Borrower.query.get_or_404(id)

    try:
        db.session.delete(borrower_to_delete)
        db.session.commit()

        flash("Borrower was deleted from database ")

        borrowers = Borrower.query.order_by(Borrower.id)
        return render_template('brwrview.html', borrowers = borrowers)

    except:
        flash("Error deleting borrower")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/libview', methods=['GET', 'POST'])
@login_required
def libview():
    #Grab all books from database
    books = Book.query.order_by(Book.id)
    return render_template('libview.html', books = books)

@app.route('/libview/<int:id>')
def booklook(id):
    book = Book.query.get_or_404(id)
    return render_template('book.html', book=book)

@app.route('/libview/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.synopsis = form.synopsis.data
        book.available = form.available.data

        db.session.add(book)
        db.session.commit()
        flash("Book information has been updated")
        return redirect(url_for('libview'))
    form.title.data = book.title
    form.author.data = book.author
    form.synopsis.data = book.synopsis
    form.available.data = book.available
    return render_template('edit_book.html', form=form)
    
@app.route('/libview/delete/<int:id>')
def delete_book(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()

        flash("Book was deleted from database ")

        books = Book.query.order_by(Book.id)
        return render_template('libview.html', books = books)

    except:
        flash("Error deleting book")



@app.route('/bookadd', methods=['GET', "POST"])
@login_required
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, synopsis=form.synopsis.data, available=form.available.data)
        #Clear the form
        form.title.data = ''
        form.author.data = ''
        form.synopsis.data = ''
        form.available.data = True

        #Add post data to database
        db.session.add(book)
        db.session.commit()

        flash("Book added to database successfully")

    return render_template("bookadd.html", form=form)


#app.route('/borroweradd', methods = ['GET', "POST"])
#def hello_world():
    


