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