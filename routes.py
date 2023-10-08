from app import app
from flask import redirect, render_template, url_for, request, flash, session
from products import new_product
import query as q 
from users import check_user_password, new_user, remove_user
from orders import add_order_to_database
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
            session['username'] = user
            session['user_position'] = q.user_position(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Username/password did not match!", category="danger")

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
    product_count = q.count_products()
    inventory_value = q.sum_inventory_value()
    revenue = q.sum_sales()
    best_sel = q.best_sellers()
    most_items = q.most_items_perwarehouse
    #low_inv = q.low_inventory()

    return render_template("dashboard.html", product_count=product_count, most_items=most_items, inventory_value=inventory_value, revenue=revenue, best_sel=best_sel)

@app.route("/neworder", methods=["GET", "POST"])
@login_required
def neworder():
    form = forms.new_order()
    new_order_valitated = False

    if form.validate_on_submit() and request.method == "POST":
        customer = request.form["customer"]
        address = request.form["address"]
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        if q.product_query(product_id):
            new_order_valitated = True
            
            if q.count_product_quantity(product_id) < quantity:
                new_order_valitated = False
                flash("Not enough inventory for order!")

        else:
            flash("Product not found.")

        if new_order_valitated:
            sale_person_id = q.user_exists(session["username"])[0]
            add_order_to_database(customer, address, product_id, quantity, sale_person_id)
            

    return render_template("neworder.html", form=form)

@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    form = forms.Product_search()

    if request.method == 'POST':
        product = request.form["product_search"]
        result = q.product_search(product)
        return render_template("products.html", count=len(result), products=result, quantities = None,  form=form)

    else:
        product_list = q.all_products()
        product_quantities = q.count_all_product_quantities()
        return render_template("products.html", count=len(product_list), products=product_list, quantities = product_quantities,  form=form)

@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    form = forms.Order_search()

    if request.method == 'POST':
        pass
    else:
        orders_list = q.all_orders()
        totals = q.sum_total()
    return render_template("orders.html", count=len(orders_list), orders=orders_list, totals=totals, form=form)

@app.route("/order_details/<order_id>")
@login_required
def order_details(order_id):
    order = q.order_details_by_id(order_id)
    products_list = q.products_in_order(order_id)

    return render_template("order_details.html", order=order, count=len(products_list), products_list=products_list)

@app.route("/order_add/<order_id>")
@login_required
def order_add(order_id):
    pass
    return render_template("order_details.html")

@app.route("/newuser", methods=["GET", "POST"])
@login_required
def newuser():
    form = forms.new_user()
    if form.validate_on_submit() and request.method == "POST":
        user = request.form["username"]
        first = request.form["first"]
        last = request.form["last"]
        password = request.form["password1"]    
        user_position = request.form["position"]

        if not q.user_exists(user):
            new_user(user, first, last, password, user_position)
            flash("New user added!")
            return redirect(url_for("newuser"))

        else:
            flash("User name already exists.")


    return render_template("newuser.html", form=form)

@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
    users = q.users_all()
    if request.method == 'POST':
        
        id = request.form["button_id"]
        user_id = q.user_exists(session["username"])
        
        if id != user_id:
            print(id)
            remove_user(id)

        return redirect(url_for("users"))
    
    return render_template("users.html", count=len(users), users=users)

@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")

@app.route("/product_details/<product_id>")
@login_required
def product_details(product_id):
    product = q.product_query(product_id)
    product_quantities = q.count_product_quantity(product_id)
    warehouses = q.count_product_per_warehouse(product_id)

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