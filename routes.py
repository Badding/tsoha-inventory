from app import app
from flask import redirect, render_template, url_for, request, flash, session
#from forms import New_product
from products import new_product
from query import product_query, count_all_product_quantities, all_products, count_product_quantity, product_search, count_product_per_warehouse
from users import check_user_password
from functools import wraps
import forms

#this functifills the testing enviroment
from test_items import create_test_db


@app.route("/", methods=["GET", "POST"])
def index():
    form = forms.login()
    if form.validate_on_submit():
        user = request.form["username"]
        password = request.form["password"]       
        success = check_user_password(user, password)

        if success:
            flash("You are logged in", category="success")
            session['username'] = user
            return redirect(url_for('dashboard'))

        else:
            flash("Invalid username/password!", category="danger")

    if "test" in request.form:
        create_test_db()
        
    return render_template("index.html", form=form)

# Define a custom decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "username" in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/logout")
@login_required
def logout():
    del session["username"]  
    return redirect("/")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    form = forms.Product_search()

    if request.method == 'POST':
        product = request.form["product_search"]
        result = product_search(product)
        print(len(result))
        return render_template("products.html", count=len(result), products=result, quantities = None,  form=form)

    else:
        product_list = all_products()
        product_quantities = count_all_product_quantities()
        return render_template("products.html", count=len(product_list), products=product_list, quantities = product_quantities,  form=form)

@app.route("/orders")
@login_required
def orders():
    return render_template("orders.html")

@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")

@app.route("/product_details/<product_id>")
@login_required
def product_details(product_id):
    product = product_query(product_id)
    product_quantities = count_product_quantity(product_id)
    warehouses = count_product_per_warehouse(product_id)

    return render_template("product_details.html", product = product, quantity = product_quantities, warehouses = warehouses)
    
@app.route("/newproduct", methods=["GET", "POST"])
@login_required
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