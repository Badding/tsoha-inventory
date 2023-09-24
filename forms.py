from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField,DecimalField
from wtforms.validators import DataRequired

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
