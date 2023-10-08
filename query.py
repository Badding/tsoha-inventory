from db import db
from flask import session
from sqlalchemy.sql import text

def product_query(id):
    sql = text("SELECT * FROM Products WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def product_by_name(name):
    sql = text("SELECT id FROM products WHERE name=(:name)")
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()[0]

def product_search(name):
    sql = text("SELECT * FROM products WHERE name ILIKE '%' || :name || '%'")
    result = db.session.execute(sql, {"name":name})
    return result.fetchall()

def all_products():
    sql = text("SELECT * FROM products ORDER BY name")
    result = db.session.execute(sql)
    return result.fetchall()

def manufacturer_query(manufacturer):
    sql = text("SELECT name, address FROM Supplier WHERE name (:manufacturer)")
    result = db.session.execute(sql, {"name":manufacturer})
    return result.fetchall()

def find_supplier(name):
    sql = text("SELECT id FROM Suppliers WHERE name=(:name)")
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()[0]

#warehouse queries
def find_warehouse(name):
    sql = text("SELECT id FROM Warehouses WHERE name=(:name)")
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()[0]

def count_all_product_quantities():
    sql = text("""
                SELECT p.id, SUM(ii.unit_size) AS total_quantity 
                FROM Products p 
                LEFT JOIN Inventory_item ii ON p.id=ii.product_id 
                GROUP BY p.id
                """)

    result = db.session.execute(sql)
    return result.fetchall()

def count_product_quantity(id):
    sql = text("SELECT SUM(unit_size) FROM inventory_item WHERE product_id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def count_product_per_warehouse(id):
    sql = text("""
                SELECT wh.name, SUM(ii.unit_size) 
                FROM inventory_item ii 
                LEFT JOIN warehouses wh ON ii.location_id=wh.id 
                WHERE ii.product_id=:id 
                GROUP BY wh.id;
                """)

    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def count_order_total(product_id, quantity):
    sql = text("SELECT price FROM Products WHERE id=:product_id")     
    result = db.session.execute(sql, {"product_id":product_id})
    return result.fetchall()[0] * quantity

#User queries

def users_all():
    sql = text("SELECT * FROM users ORDER BY username")
    result = db.session.execute(sql)
    return result.fetchall()

def user_position(name):
    sql = text("SELECT position FROM users WHERE username=(:name)")
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()[0]

def user_exists(name):
    sql = text("SELECT id FROM users WHERE username=(:name)")
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()

#Orders

def all_orders():
    sql = text("""SELECT
                    s.id AS sale_id,
                    c.name AS customer_name,
                    s.address AS sale_address,
                    s.sale_date,
                    u.first_name,
                    u.last_name,
                    s.total_amount
                FROM
                    Sales s
                INNER JOIN
                    Users u ON s.sales_person_id = u.id
                INNER JOIN
                    Customers c ON s.customer_id = c.id;
            """)
    result = db.session.execute(sql)
    return result.fetchall()

def order_details_by_id(order_id):
    sql = text("""SELECT
                    s.id AS sale_id,
                    c.name AS customer_name,
                    s.address AS sale_address,
                    s.sale_date,
                    u.first_name,
                    u.last_name,
                    s.total_amount
                FROM
                    Sales s
                INNER JOIN
                    Users u ON s.sales_person_id = u.id
                INNER JOIN
                    Customers c ON s.customer_id = c.id
                WHERE s.id = :order_id;
            """)
    result = db.session.execute(sql,{"order_id":order_id})
    return result.fetchone()

def products_in_order(order_id):
    sql = text("""SELECT
                    p.name AS product_name,
                    sd.quantity
                FROM
                    Salesdetail sd
                INNER JOIN
                    Products p ON sd.product_id = p.id
                WHERE
                    sd.order_id = :order_id;
            """)
    result = db.session.execute(sql,{"order_id":order_id})
    return result.fetchall()

def sum_total():
    sql = text("""SELECT
                s.id AS sale_id,
                SUM(p.price * sd.quantity) AS total_cost
            FROM
                Sales AS s
            JOIN
                Salesdetail AS sd ON s.id = sd.order_id
            JOIN
                Products AS p ON sd.product_id = p.id
            GROUP BY
                s.id;
            """)
    result = db.session.execute(sql)
    return result.fetchall()


#customer

def find_customer(customer):
    sql = text("SELECT * FROM Customers WHERE LOWER(name)=LOWER((:customer))")
    result = db.session.execute(sql, {"customer":customer})
    return result.fetchone()