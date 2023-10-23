from app import app
from flask import redirect, render_template, url_for, request, flash, session, abort
from products import new_product
import query as q 
from users import check_user_password, new_user, remove_user, change_password
from orders import add_order_to_database, modify_order_add_product
import warehouse as wh
from functools import wraps
import forms
import secrets

#this module handles creation of the test database
from test_items import create_test_db

@app.route("/", methods=["GET", "POST"])
def index():
    form = forms.login()

    #if session["username"]:
    #    return redirect(url_for("dashboard"))

    if form.validate_on_submit():
        user = request.form["username"]
        password = request.form["password"]       
        success = check_user_password(user, password)

        if success:
            session['username'] = user
            session['user_position'] = q.user_position(user)
            session["csrf"] = secrets.token_hex(16)

            return redirect(url_for('dashboard'))
        else:
            flash("Username/password did not match!", category="danger")

    if "test" in request.form:
        create_test_db()
        
    return render_template("index.html", form=form)

# Define a custom decorator to protect routes - login needed
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
    inv_per_wh = q.inventory_per_warehouse()
    inv_zero = q.product_count_zero()
    low_inv = q.low_inventory()

    return render_template("dashboard.html",
                            product_count=product_count,
                            most_items=most_items,
                            inventory_value=inventory_value,
                            revenue=revenue,
                            best_sel=best_sel,
                            inv_per_wh=inv_per_wh,
                            inv_zero=inv_zero,
                            )

@app.route("/neworder", methods=["GET", "POST"])
@login_required
def neworder():
    form = forms.new_order()
    new_order_valitated = False

    if form.validate_on_submit() and request.method == "POST":

        if session["csrf"] != request.form["csrf"]:  
            abort(403)
        
        customer = request.form["customer"]
        address = request.form["address"]
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        if q.product_query(product_id):
            new_order_valitated = True
            prod_in_warehouses = q.count_product_quantity(product_id)

            if prod_in_warehouses < quantity:
                new_order_valitated = False
                flash(f"Not enough inventory for the order! Only {prod_in_warehouses} in stock")

        else:
            flash("Product not found.")

        if new_order_valitated:
            print("validates")
            sale_person_id = q.user_exists(session["username"])[0]
            order_id = add_order_to_database(customer, address, product_id, quantity, sale_person_id)
            
            return redirect(url_for("order_details", order_id=order_id))


    return render_template("neworder.html", form=form)

@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    sorting_properties = {"name": "p.name",
                        "id": "p.id",
                        "quantity": "total_quantity",
                        "manufacturer": "p.manufacturer",
                        "price": "p.price"}
    order = {"ascend": " asc", "descend": " desc"}

    form = forms.Product_sort()
    sort_by, asc_or_desc = sorting_properties["name"], order["ascend"]
    product = ""

    if request.method == 'POST':
        if session["csrf"] != request.form["csrf"]:
            abort(403)
    
        product = request.form["product_search"]
        
        s = request.form["order"]
        a = request.form["asc_or_desc"]
        if s in sorting_properties:
            sort_by = sorting_properties[s]
        if a in order:
            asc_or_desc = order[a]
        
    else:
        if form.errors:
            print(form.errors)

    product_list = q.product_search_with_quantities(sort_by, asc_or_desc, product)  
    
    return render_template("products.html",
                            products=product_list,
                            form=form,)

@app.route("/products_search", methods=["GET", "POST"])
@login_required
def products_search():
    search = forms.Product_search()
    sorting_form = forms.Product_sort()
    sort_by, asc_or_desc = "name", " asc"
    
    if "search" in request.values and request.method == 'POST':
            product = request.form["product_search"]
            result = q.product_search_with_quantities(sort_by, product)
    
    sort_by = request.form["order"]
    asc_or_desc = request.form["asc_or_desc"]

    return render_template("products.html",
                            products=result,
                            search=search,
                            sorting_form=sorting_form)

@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    form = forms.Order_search()
    sorting_properties = {"name": "c.name", "id": "s.id", "address": "s.address", "seller": "u.last_name", "total": "total"}
    order = {"ascend": " asc", "descend": " desc"}
    sort_by, asc_or_desc = sorting_properties["name"], order["ascend"]
    order_search = ""
    s = "customer"

    if request.method == 'POST':
        if session["csrf"] != request.form["csrf"]:
            abort(403)

        order_search = request.form["order_search"]
        s = request.form["order"]
        a = request.form["asc_or_desc"]

        if s in sorting_properties:
            sort_by = sorting_properties[s]
        if a in order:
            asc_or_desc = order[a]

    else:
        pass
        if form.errors:
            print(form.errors)

    orders_list = q.all_orders_with_sort_and_search(sort_by, asc_or_desc, order_search)

    return render_template("orders.html",
                            orders=orders_list,
                            form=form)

@app.route("/order_details/<order_id>")
@login_required
def order_details(order_id):
    order = q.all_orders_with_sort_and_search("s.id", " asc", order_id)
    products_list = q.products_in_order(order_id)
    
    return render_template("order_details.html", order=order, products_list=products_list)

@app.route("/order_add/<order_id>", methods=["GET", "POST"])
@login_required
def order_add(order_id):
    form = forms.add_product_to_order()
    new_order_valitated = False

    if form.validate_on_submit() and request.method == "POST":

        if session["csrf"] != request.form["csrf"]:
            abort(403)

        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        if q.product_query(product_id):
            new_order_valitated = True
            prod_in_warehouses = q.count_product_quantity(product_id)

            if  prod_in_warehouses < quantity:
                new_order_valitated = False
                flash(f"Not enough inventory for the order! Only {prod_in_warehouses} in stock")

        else:
            flash("Product not found.")

        if new_order_valitated:
            modify_order_add_product(order_id, product_id, quantity)         
            return redirect(url_for("order_details", order_id=order_id))
    else:
        if form.errors:
            print(form.errors)
    return render_template("order_add.html", form=form)

@app.route("/newuser", methods=["GET", "POST"])
@login_required
def newuser():
    form = forms.new_user()
    if form.validate_on_submit() and request.method == "POST":
        
        if session["csrf"] != request.form["csrf"]:
            abort(403)

        user = request.form["username"]
        first = request.form["first"]
        last = request.form["last"]
        password = request.form["password1"]    
        user_position = request.form["position"]
        print("help")
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
            remove_user(id)

        return redirect(url_for("users"))
    
    return render_template("users.html", count=len(users), users=users)

@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    form = forms.Change_password()
    
    if form.validate_on_submit() and request.method == "POST":

        if session["csrf"] != request.form["csrf"]:
            abort(403)
        password = request.form["password2"]
        user_id = q.user_exists(session["username"])[0]

        change_password(password, user_id)
        return redirect(url_for("dashboard"))


    return render_template("user.html", form=form)

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
    if form.validate_on_submit() and request.method == "POST":
    
        if session["csrf"] != request.form["csrf"]:        
            abort(403)
        
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

        if not q.product_by_name(product):
            new_product(product_data)
            return redirect(url_for("products"))

    return render_template("newproduct.html", form=form)

@app.route("/inventory_add", methods=["GET", "POST"])
@login_required
def inventory_add():
    form = forms.add_inventory()
    products = q.all_products("id")
    warehouses = q.warehouses()
    suppliers = q.all_suppliers()
    product_list =  [(pr[0], pr[1])for pr in products]
    wh_list =  [(wh[0], wh[1])for wh in warehouses]
    sup_list = [(sup[0], sup[1])for sup in suppliers]
    form.warehouse.choices = wh_list
    form.supplier.choices = sup_list
    form.product.choices = product_list
    
    if form.validate_on_submit() and request.method == "POST":

        if session["csrf"] != request.form["csrf"]:      
            abort(403)      

        product_id = request.form["product"]
        warehouse_id = request.form["warehouse"]
        supplier_id = request.form["supplier"]
        quantity = request.form["quantity"]

        if not q.product_query(product_id):
                flash("Product not found!")
        else:
            
            wh.add_inventory_to_warehouse(
                product_id,
                warehouse_id,
                supplier_id,
                quantity
            )

    return render_template("inventory_add.html", form=form)

@app.route("/warehouses", methods=["GET", "POST"])
@login_required
def warehouses():
    warehouses = q.warehouses()

    return render_template("warehouses.html",
                        warehouses=warehouses)

@app.route("/warehouse_details/<warehouse_id>")
@login_required
def warehouse_details(warehouse_id):
    warehouse = q.warehouse_inventory(warehouse_id)
    return render_template("warehouse_details.html",
                        warehouse=warehouse)

@app.route("/warehouse_create", methods=["GET", "POST"])
@login_required
def warehouse_create():
    form = forms.Create_warehouse()
    if form.validate_on_submit() and request.method == "POST":

        if session["csrf"] != request.form["csrf"]: 
            abort(403)      
            
        warehouse = request.form["name"]
        
        if not q.find_warehouse(warehouse): 
            
            wh.create_warehouse(warehouse)
            return redirect(url_for("warehouses"))
        
        else:
            flash("Warehouse already exists")

    return render_template("warehouse_create.html",
                        form=form)

@app.route("/supplier_create", methods=["GET", "POST"])
@login_required
def supplier_create():
    form = forms.Create_supplier()
    if form.validate_on_submit() and request.method == "POST":

        if session["csrf"] != request.form["csrf"]: 
            abort(403)      
            
        supplier = request.form["name"]
        address = request.form["address"]

        if not q.find_supplier(supplier): 
            
            wh.create_supplier(supplier, address)
            return redirect(url_for("warehouses"))
        
        else:
            flash("supplier already exists")
    else:
        print(form.errors)
    return render_template("supplier_create.html",
                        form=form)
