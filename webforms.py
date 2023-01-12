from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, EmailField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Email
from wtforms.widgets import TextArea

#Form for adding new borrower
class BorrowForm(FlaskForm):
    book_id = IntegerField("book id", validators=[DataRequired(), NumberRange(min=1, max=100)])
    borrower_id = IntegerField("borrower field", validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField("Submit")

#Form for adding borrower
class BorrowerForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email("Enter a valid email address")], widget=TextArea() )
    apartment_number = StringField("Apartment Number", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    verify_password_hash = PasswordField("Re-enter Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Form to search books or borrowers
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Form to add book
class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    synopsis = StringField("Synopsis", validators=[DataRequired()], widget=TextArea())
    available = BooleanField("Availability", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Form to add user
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email("Enter a valid email address")], widget=TextArea() )
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Form used for login
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Enter a valid email address")], widget=TextArea() )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

#Form for choice of login
class LoginChoiceForm(FlaskForm):
    librarian_login = SubmitField("Librarian Login")
    borrower_login = SubmitField("Reader Login") 