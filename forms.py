from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, DecimalField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

class New_product(FlaskForm):
    product = StringField(label='Product:', validators=[DataRequired()])
    manufacturer = StringField(label='Manufacturer:')
    description = TextAreaField(label='Description:')
    price = DecimalField(label='Price:', places='2')
    create = SubmitField(label="Add Product")

class New_manufacturer(FlaskForm):
    manufacturer = StringField(label='Manufacturer:')
    create = SubmitField(label="Add Product")

class Product_search(FlaskForm):
    property = SelectField(label="Search by", choices=[("name", "Name"), ("id", "ID"), ("manufacturer", "Manufacturer")])
    product_search = StringField()
    search = SubmitField()

class Product_sort(FlaskForm):
    order = SelectField(label="Order by", choices=[
        ("name", "Name"),
        ("id", "ID"),
        ("quantity", "Quantity"),
        ("manufacturer", "Manufacturer"),
        ("price", "Price at least")
        ])
    property = SelectField("Search by", choices=[("name", "Name"), ("id", "ID"), ("manufacturer", "Manufacturer")])
    product_search = StringField()
    asc_or_desc = SelectField(label="Ascend or descend", choices=[("ascend", "Ascend"), ("descend", "Descend")])
    sort = SubmitField(label="Search and sort")

class Order_search(FlaskForm):
    order = SelectField(label="Order by", choices=[
        ("name", "Customer"),
        ("id", "ID"),
        ("address", "Address"),
        ("seller", "Seller"),
        ])
    property = SelectField("Search by", choices=[("name", "Name"), ("id", "ID"), ("address", "Address")])
    order_search = StringField()
    asc_or_desc = SelectField(label="Ascend or descend", choices=[("ascend", "Ascend"), ("descend", "Descend")])
    sort = SubmitField(label="Search and sort")

class login(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class new_user(FlaskForm):
    username = StringField(label='Username, atleast 6 characters', validators=[Length(min=6), DataRequired()])
    position = SelectField(label='Select Role',
                        choices=[("admin", "Admin"), ("manager", "Manager"), ("sales", "Sales")],
                        validators=[DataRequired()])
    
    first = StringField(label='First Name', validators=[DataRequired()])
    last = StringField(label='Last Name', validators=[DataRequired()])
    password1 = PasswordField(label="Password, atleast 8 characters", validators=[DataRequired()])
    password2 = PasswordField(label="Retype password", validators=[EqualTo("password1"), Length(min=8),DataRequired()])
    submit = SubmitField(label="Add new user")

class new_order(FlaskForm):
    customer = StringField(label='Customer:', validators=[DataRequired()])
    address = StringField(label='Address:', validators=[DataRequired()])
    product_id = IntegerField(label='Product id:', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity:', validators=[NumberRange(min=1),DataRequired()])

    """ For better sale form
    product_search = StringField(label='Search product by name:')
    id_search = IntegerField(label='Search product by id:')
    search_name = SubmitField(label="Search name")
    search_id = SubmitField(label="Search id")
    """
    submit = SubmitField(label="Submit sale")

class add_product_to_order(FlaskForm):
    product_id = IntegerField(label='Product id:', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity:', validators=[NumberRange(min=1),DataRequired()])
    submit = SubmitField(label="Add product")
