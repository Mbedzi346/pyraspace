from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Optional, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit1 = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Email('Invalid Email Address')], render_kw={"placeholder": "Email Address"})
    phone_number = StringField('Phone Number', validators=[Regexp('(^(\+27|0)\d{9}$)', message='Invalid phone number format. (i.e 0123456789 or +27123456789)')])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    #confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',message= 'Passwords must match.')])
    submit2 = SubmitField('Sign Up!')

class SearchForm(FlaskForm):
    search_query = StringField('Search Query', validators=[DataRequired()])
    submit = SubmitField('Search')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Example: Modern Business Statistics'})
    module_code = StringField('Module Code', validators=[Optional()], render_kw={'placeholder' : 'STK 110/120'})
    description = TextAreaField('Description', validators=[DataRequired(),Regexp('(?!(\+27|0)\d{9}1)')], render_kw={'placeholder': 'Example: 4th Edition. Minor wear and tear to the cover, barely used.'})
    price = IntegerField('Price', validators=[DataRequired(message='Digits only. i.e 400, not R400')], render_kw={'placeholder': 'Example: 400'})
    location = SelectField('Location', choices=[('up_hatfield', 'University of Pretoria, Hatfield'), ('up_groenkloof', 'University of Pretoria, Groenkloof'),
                                                ('up_mamelodi', 'University of Pretoria, Mamelodi'), ('up_prinshof', 'University of Pretoria, Prinshof'),('univen', 'University of Venda')])
    category = SelectField('Category', choices=[('books', 'Books'), ('electronics', 'Electronics'), ('other', 'Other')])
    image =  FileField('Product Photo', validators=[FileRequired()])
    submit = SubmitField('Add Product')

class RequestForgetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    submit = SubmitField('Request New Password')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')

class UpdateProductForm(FlaskForm):
    title = StringField('Title', validators=[Optional()], render_kw={'placeholder': 'Leave blank if you are not making any changes to the title'})
    description = TextAreaField('Description', validators=[Optional()],render_kw={'placeholder': 'Leave blank if you are not making any changes to the description'})
    price = IntegerField('Price', validators=[Optional()],render_kw={'placeholder': 'Leave blank if you are not making any changes to the price'})
    submit = SubmitField('Update')

class AdminLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
