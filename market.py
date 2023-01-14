from enum import unique
from pydoc import synopsis
from flask import Flask, request, render_template, url_for, flash,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import timedelta
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from webforms import BorrowForm, BorrowerForm, SearchForm, BookForm, UserForm, LoginForm
from flask_migrate import Migrate
import uuid as uuid
from sqlalchemy import update
from sqlalchemy import ForeignKey


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dangerzone@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "whatgoesupmustneverstayupforthedevillooksforanomalousbasterds101"

#Login, Authenitcation and Registeration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):  
    return Users.query.get(int(user_id)) or Borrower.query.get(int(user_id))


#Searching
@app.context_processor
def base():
    form = SearchForm() 
    return dict(form=form)

#Models

#Borrower Model
class Borrower (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    late_returns = db.Column(db.Integer, nullable = False, default=0)
    superuser = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128), nullable=False)
    #Backref
    borrow = db.relationship('Borrow', backref='borrower')


#Book Model
class Book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.BLOB, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    #Backref
    borrow = db.relationship('Borrow', backref='book')


#User Model
class  Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    superuser = db.Column(db.Boolean, nullable=False, default=True)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
      raise AttributeError('password is unreadable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


#Borrow Model
class Borrow (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.Date, default=date.today())
    book_id = db.Column(db.Integer, ForeignKey(Book.id))
    borrower_id = db.Column (db.Integer, ForeignKey(Borrower.id))
    overdue = db.Column(db.Boolean, nullable = False, default=False)
    daysleft = db.Column(db.Integer, nullable = False, default=7)
    return_date = db.Column(db.Date, nullable=False, default=date.today() + timedelta(days=20))
    returned = db.Column(db.Boolean, nullable=True, default=False) 


#Login choice page
@app.route('/', methods=['GET', 'POST'])
def loginchoice(): 
    return render_template('loginchoicepage.html')

#Borrower login page
@app.route('/readerlogin', methods=['GET', 'POST'])
def readerlogin():
    form = LoginForm()
    if form.validate_on_submit():
        borrower = Borrower.query.filter_by(email=form.email.data).first()
        if borrower:
            #check hash
            if check_password_hash(borrower.password_hash, form.password.data):
                login_user(borrower)
                return redirect(url_for('readerbookview'))
            else:
                flash("WRONG PASSWORD TRY AGAIN") 
        else:
            flash("USER DOES NOT EXIST")

    return render_template('librarianlogin.html', form=form)


#Reader registeration
@app.route('/register', methods=['GET', "POST"])
def borroweradd():
    form = BorrowerForm()
    if form.validate_on_submit():
        borrower = Borrower.query.filter_by(email=form.email.data).first()
        if borrower is None:
            if form.password_hash.data == form.verify_password_hash.data:
                hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
                borrower = Borrower(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,password_hash=hashed_pw)
            
                form.first_name.data = ''
                form.last_name.data = ''
                form.email.data = ''
                form.password_hash.data = ''

                #Add borrower data to database
                db.session.add(borrower)
                db.session.commit()
            else:
                flash("Passwords do not match")


        flash("Borrower added to database successfully")
        return redirect(url_for('loginchoice'))
    else:
        flash("Please enter valid information")


    return render_template("registeration.html", form=form)


#Librarian Login page
@app.route('/librarianlogin', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            #check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('bookview'))
            else:
                flash("WRONG PASSWORD TRY AGAIN") 
        else:
            flash("USER DOES NOT EXIST")

    return render_template('librarianlogin.html', form=form)

#Adding User
@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    #Hashing Password
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(email=form.email.data, name=form.name.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
    
    return render_template ( "adduser.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('loginchoice'))

#Books

#Add book
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

        #Add book data to database
        db.session.add(book)
        db.session.commit()

        flash("Book added to database successfully")

    return render_template("bookadd.html", form=form)

#List of books
@app.route('/books', methods=['GET', 'POST'])
@login_required
def bookview():
    #Grab all books from database
    books = Book.query.order_by(Book.id)
    return render_template('bookview.html', books = books)

#View book details for librarian 
@app.route('/books/<int:id>')
@login_required
def viewbook(id):
    book = Book.query.get_or_404(id)
    return render_template('book.html', book=book)

#View book details for reader
@app.route('/readerbooks/<int:id>')
@login_required
def readerbook(id):
    book = Book.query.get_or_404(id)
    return render_template('readerbook.html', book=book)

#Edit book details
@app.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('books'))
    form.title.data = book.title
    form.author.data = book.author
    form.synopsis.data = book.synopsis
    form.available.data = book.available
    return render_template('edit_book.html', form=form)

#Delete book   
@app.route('/books/delete/<int:id>')
@login_required
def delete_book(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()

        flash("Book was deleted from database ")

        books = Book.query.order_by(Book.id)
        return render_template('bookview.html', books = books)

    except:
        flash("Error deleting book")

#Search for books
@app.route('/booksearch', methods=["POST"])
@login_required
def booksearch():
    form = SearchForm()
    books = Book.query

    if form.validate_on_submit(): #If user is librarian 
        
        viewbook.searched = form.searched.data

        books = books.filter(Book.title.like('%' + viewbook.searched + '%'))
        books = books.order_by(Book.title).all()
     
        return render_template("booksearch.html", form=form, searched = viewbook.searched, books = books)

@app.route('/readerbooksearch', methods=["POST"])
@login_required
def readerbooksearch():
    form = SearchForm()
    books = Book.query

    if form.validate_on_submit(): #If user is librarian 
        
        viewbook.searched = form.searched.data

        books = books.filter(Book.title.like('%' + viewbook.searched + '%'))
        books = books.order_by(Book.title).all()
     
        return render_template("readerbooksearch.html", form=form, searched = viewbook.searched, books = books)


#Reader book view
@app.route('/readerbookview', methods=['GET', 'POST'])
@login_required
def readerbookview():
        #Grab all books from database
    books = Book.query.order_by(Book.id)
    return render_template('readerbookview.html', books = books)

#Borrowers

#View list of borrowers
@app.route('/borrowerview', methods=['GET', 'POST'])
@login_required
def borrowerview():
    #Grab all books from database
    borrowers = Borrower.query.order_by(Borrower.id)
    return render_template('borrowerview.html', borrowers = borrowers)

#Edit borrower details
@app.route('/borrowerview/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_borrower(id):
    borrower = Borrower.query.get_or_404(id)
    form = BorrowerForm()
    if form.validate_on_submit():
        borrower.first_name = form.first_name.data
        borrower.last_name = form.last_name.data
        borrower.email = form.email.data
        

        db.session.add(borrower)
        db.session.commit()
        flash("Book information has been updated")
        return redirect(url_for('brwrview'))
    form.first_name.data = borrower.first_name
    form.last_name.data = borrower.last_name
    form.email.data = borrower.email
    return render_template('edit_borrower.html', form=form)

#View borrower details
@app.route('/borrowerview/<int:id>', methods=['GET', 'POST'])
@login_required
def borrowerlook(id):
    borrower = Borrower.query.get_or_404(id)
    return render_template('borrowerlook.html', borrower=borrower)

#Delete borrower from database
@app.route('/borrowerview/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def borrowerdelete(id):
    borrower_to_delete = Borrower.query.get_or_404(id)

    try:
        db.session.delete(borrower_to_delete)
        db.session.commit()

        flash("Borrower was deleted from database ")

        borrowers = Borrower.query.order_by(Borrower.id)
        return render_template('borrowerview.html', borrowers = borrowers)

    except:
        flash("Error deleting borrower")

#View your borrows
@app.route('/myborrows')
@login_required
def myborrows():

    print(current_user.superuser)
    #reader = current_user.id
    myborrows = Borrow.query.filter(Borrow.borrower_id == current_user.id).all()
    return render_template('myborrows.html', myborrows = myborrows, current_user = current_user.id)


#Borrows

#Create a borrow
@app.route('/borrowadd', methods=['GET','POST'])
@login_required
def borrowadd():
    form = BorrowForm()

    print(current_user.superuser)

    if form.validate_on_submit():
        
        if  db.session.query(Book.id).filter_by(id = form.book_id.data).first() is not None and db.session.query(Borrower.id).filter_by(id = form.borrower_id.data).first() is not None:
            
            book_in_borrow = Book.query.filter_by(id = form.book_id.data).first()
            if book_in_borrow.available != False:      
                borrow = Borrow(book_id=form.book_id.data, borrower_id=form.borrower_id.data)
                #Clear the form  
                update(Book).where(Book.id == form.book_id.data).values(available=False)
                book_in_borrow.available = False
                form.book_id.data = ''
                form.borrower_id.data = '' 
               
                db.session.add(borrow)
                db.session.commit() 
                flash("Borrow added to database successfully")

            else:
                flash("Book is not available")

        else:
            flash("Please enter valid IDs")

    return render_template("borrowadd.html", form=form)

#Return a book 
@app.route('/borrowview/return/<int:id>', methods=['GET','POST'])
@login_required
def returnbook(id):
    borrow_to_confirm = Borrow.query.get_or_404(id)
    borrowed_book = Book.query.filter_by(id = borrow_to_confirm.book_id).first()
    borrower_in_borrow = Borrower.query.filter_by(id = borrow_to_confirm.borrower_id).first()

    try:
        if borrow_to_confirm.overdue == False:
            borrowed_book.available = True
            borrow_to_confirm.returned = True

            db.session.commit()

            flash("Return Successful")

            todays_date = date.today()
            borrows = Borrow.query.order_by(Borrow.id)
            for borrow in borrows:
                if (todays_date - borrow.return_date).days > 1:
                    borrow.overdue = True

            return render_template('borrowview.html', borrows = borrows, todays_date=todays_date)

        else:
            borrowed_book.available = True
            borrower_in_borrow.late_returns = borrower_in_borrow.late_returns + 1
            borrow_to_confirm.returned = True

            db.session.commit()

            flash("Return Successful, Late returns updated")

            todays_date = date.today()
            borrows = Borrow.query.order_by(Borrow.id)
            for borrow in borrows:
                if (todays_date - borrow.return_date).days > 1:
                    borrow.overdue = True

            return render_template('borrowview.html', borrows = borrows, todays_date=todays_date)

    except:

        flash("An error occured")

#View list of borrows
@app.route('/borrowview', methods=['GET','POST'])
@login_required
def borrowview():   
    #Grab all borrows from database
    todays_date = date.today()
    borrows = Borrow.query.order_by(Borrow.id)
    for borrow in borrows:
        if (todays_date - borrow.return_date).days > 1:
            borrow.overdue = True

    return render_template('borrowview.html', borrows = borrows, todays_date=todays_date)


#Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500












