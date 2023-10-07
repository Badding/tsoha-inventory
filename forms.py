from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, DecimalField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

class New_product(FlaskForm):
    product = StringField(label='Product:', validators=[DataRequired()])
    #quantity = IntegerField(label='Quantity:', validators=[DataRequired()])
    manufacturer = StringField(label='Manufacturer:')
    description = TextAreaField(label='Description:')
    price = DecimalField(label='Price:', places='2')
    #supplier = StringField(label='Supplier:')
    #change to SelectField
    #location = StringField(label='Location:')
    create = SubmitField(label="Add Product")

class New_manufacturer(FlaskForm):
    manufacturer = StringField(label='Manufacturer:')
    create = SubmitField(label="Add Product")

class Product_search(FlaskForm):
    product_search = StringField()
    search = SubmitField()

class login(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class new_user(FlaskForm):
    username = StringField(label='Username, atleast 6 characters', validators=[Length(min=6), DataRequired()])
    position = SelectField(label='Select Role', choices=[("admin", "Admin"), ("manager", "Manager"), ("sales", "Sales")], validators=[DataRequired()])
    first = StringField(label='First Name', validators=[DataRequired()])
    last = StringField(label='Last Name', validators=[DataRequired()])
    password1 = PasswordField(label="Password, atleast 8 characters", validators=[DataRequired()])
    password2 = PasswordField(label="Retype password", validators=[EqualTo("password1"), Length(min=8),DataRequired()])
    submit = SubmitField(label="Add new user")