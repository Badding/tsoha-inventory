from app import app
from flask import redirect, render_template, url_for, request
#from forms import New_product
from products import new_product
from query import product_query, count_all_product_quantities, all_products, count_product_quantity
import forms

#TEST
from test_items import create_test_db

import query 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products", methods=["GET", "POST"])
def products():
    form = forms.Product_search()
    product_list = all_products()
    product_quantities = count_all_product_quantities()

    return render_template("products.html", count=len(product_list), products=product_list, quantities = product_quantities,  form=form)

@app.route("/orders")
def orders():
    return render_template("orders.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == 'POST':
        create_test_db()
    return render_template("about.html")

@app.route("/product_details/<product_id>")
def product_details(product_id):
    product = product_query(product_id)
    product_quantities = count_product_quantity(product_id)

    return render_template("product_details.html", product = product, quantity = product_quantities)
    
@app.route("/newproduct", methods=["GET", "POST"])
def newproduct():
    form = forms.New_product()
    
    ### TODO advanced validation
    if form.validate_on_submit():
        product = request.form["product"]
        price = request.form["price"]
        manufacturer = request.form["manufacturer"]
        description = request.form["description"]
        product_data = {
            "product" : product,
            "price" : price,
            "manufacturer" : manufacturer,
            "description" : description
        }
        
        
        new_product(product_data)
        return redirect(url_for("products"))
    else:
        print(form.errors)
        print("new product form did not pass validation")
    return render_template("newproduct.html", form=form)