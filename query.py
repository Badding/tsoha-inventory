from db import db
from flask import session
from sqlalchemy.sql import text
from error_handling import query_wrap

def product_query(id):
    sql = "SELECT * FROM Products WHERE id=:id"
    values = {"id": id}
    result = query_wrap(sql,values)
    return result.fetchone()

def product_by_name(name):
    sql = "SELECT id FROM products WHERE name=(:name)"
    values = {"name": name}
    result = query_wrap(sql,values)
    return result.fetchone()[0]

def product_search(name):
    sql = "SELECT * FROM products WHERE name ILIKE '%' || :name || '%'"
    values = {"name": name}
    result = query_wrap(sql,values)
    return result.fetchall()

def product_search_with_quantities(sort_by, name):
    sql = f"""
        SELECT p.id, p.name, SUM(ii.unit_size) AS total_quantity, p.manufacturer, p.price
        FROM Products p
        LEFT JOIN Inventory_item ii ON p.id = ii.product_id 
        WHERE name ILIKE '%' || :name || '%'
        GROUP BY p.id
        ORDER BY {sort_by};
    """
    values = {"name": name}
    result = query_wrap(sql, values)
    return result.fetchall()

def all_products(sort_by):
    sql = f"SELECT * FROM products ORDER BY {sort_by}"
    result = query_wrap(sql, None)
    return result.fetchall()

def all_products_and_quantities(sort_by):
    sql = f"""
    SELECT p.id, p.name, SUM(ii.unit_size) AS total_quantity, p.manufacturer, p.price
    FROM Products p 
    LEFT JOIN Inventory_item ii ON p.id = ii.product_id 
    GROUP BY p.id
    ORDER BY {sort_by};
    """
    result = query_wrap(sql, None)
    return result.fetchall()

def manufacturer_query(manufacturer):
    sql = "SELECT name, address FROM Supplier WHERE name (:manufacturer)"
    values = {"manufacturer": manufacturer }
    result = query_wrap(sql,values)
    return result.fetchall()

def find_supplier(name):
    sql = "SELECT id FROM Suppliers WHERE name=(:name)"
    values = {"name": name}
    result = query_wrap(sql,values)
    return result.fetchone()[0]

def count_products():
    sql = "SELECT COUNT(*) AS product_count FROM Products"
    result = query_wrap(sql, None)
    return result.fetchone()[0]

def sum_inventory_value():
    sql = """
    SELECT SUM(ii.unit_size * p.price) AS total_inventory_value
    FROM Inventory_item AS ii
    JOIN Products AS p ON ii.product_id = p.id
    """
    result = query_wrap(sql, None)
    return result.fetchone()[0]

def best_sellers():
    sql = """
    SELECT p.name, SUM(sd.quantity) AS total_quantity_sold
    FROM Products AS p
    JOIN Salesdetail AS sd ON p.id = sd.product_id
    GROUP BY p.name
    ORDER BY total_quantity_sold DESC
    LIMIT 5
    """
    result = query_wrap(sql, None)
    return result.fetchall()

#warehouse queries

def most_items_perwarehouse():
    sql = """
    SELECT w.name AS warehouse_name, COUNT(*) AS item_count
    FROM Warehouses w
    INNER JOIN Inventory_item i ON w.id = i.location_id
    GROUP BY w.name
    ORDER BY item_count DESC
    LIMIT 1;
    """
    result = query_wrap(sql, None)
    return result.fetchall()

def find_warehouse(name):
    sql = "SELECT id FROM Warehouses WHERE name=(:name)"
    values = {"name": name}
    result = query_wrap(sql,values)
    return result.fetchone()[0]

def count_all_product_quantities():
    sql = """
    SELECT p.id, SUM(ii.unit_size) AS total_quantity 
    FROM Products p 
    LEFT JOIN Inventory_item ii ON p.id=ii.product_id 
    GROUP BY p.id
    ORDER BY total_quantity
    """
    result = query_wrap(sql,None)
    return result.fetchall()

def count_product_quantity(id):
    sql = "SELECT SUM(unit_size) FROM inventory_item WHERE product_id=:id"
    values = {"id": id}
    result = query_wrap(sql, values)
    return result.fetchone()[0]

def count_product_per_warehouse(id):
    sql = """
    SELECT wh.name, SUM(ii.unit_size) 
    FROM inventory_item ii 
    LEFT JOIN warehouses wh ON ii.location_id=wh.id 
    WHERE ii.product_id=:id 
    GROUP BY wh.id;
    """
    values = {"id":id}
    result = query_wrap(sql, values)
    return result.fetchall()

def count_order_total(product_id, quantity):
    sql = "SELECT price FROM Products WHERE id=:product_id"
    values = {"product_id":product_id}
    result = query_wrap(sql, values)
    return result.fetchall()[0] * quantity

def low_inventory():
    sql = """
    SELECT p.name, ii.unit_size
    FROM Products AS p
    JOIN Inventory_item AS ii ON p.id = ii.product_id
    WHERE ii.unit_size < 150
    """
    result = query_wrap(sql, None)
    return result.fetchall()

#User queries

def users_all():
    sql = "SELECT * FROM users ORDER BY username"
    result = query_wrap(sql, None)
    return result.fetchall()

def user_position(name):
    sql = "SELECT position FROM users WHERE username=(:name)"
    values = {"name":name}
    result = query_wrap(sql, values)
    return result.fetchone()[0]

def user_exists(name):
    sql = "SELECT id FROM users WHERE username=(:name)"
    values = {"name":name}
    result = query_wrap(sql, values)
    return result.fetchone()

#Orders

def all_orders():
    sql = """
    SELECT
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
    """
    result = query_wrap(sql, None)
    return result.fetchall()


def all_orders_with_search(sort_by, asc_or_desc, string):
    values = None
    where = ""
    sql = """
    SELECT
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
    """
    if sort_by == "c.name":
        where = f"WHERE c.name ILIKE '%' || :value || '%'"
        values = {"value": string}
    elif sort_by == "s.id":
        where = f"WHERE s.id = (:value)"
        values = {"value": string}
    elif sort_by == "s.address":
        where = f"WHERE s.address ILIKE '%' || :value || '%'"
        values = {"value": string}
    elif sort_by == "u.last_name":
        where = f"""WHERE u.first_name ILIKE '%' || :value || '%'
                OR u.last_name ILIKE '%' || :value || '%'"""
        values = {"value": string}

    end = f" ORDER BY {sort_by + asc_or_desc};"

    sql += where + end
    #print(sql)
    result = query_wrap(sql, values)
    return result.fetchall()

def all_orders_with_sort_and_search(sort_by, asc_or_desc, string):
    values = None
    where = ""
    sql = """WITH TotalCosts AS (
    SELECT
        s.id AS sale_id,
        SUM(p.price * sd.quantity) AS total_cost
    FROM
        Sales AS s
    JOIN
        Salesdetail AS sd ON s.id = sd.order_id
    JOIN
        Products AS p ON sd.product_id = p.id
    GROUP BY
        s.id
    )
    SELECT
        s.id AS sale_id,
        c.name AS customer_name,
        s.address AS sale_address,
        s.sale_date,
        u.first_name,
        u.last_name,
        s.total_amount,
        tc.total_cost
    FROM
        Sales s
    INNER JOIN
        Users u ON s.sales_person_id = u.id
    INNER JOIN
        Customers c ON s.customer_id = c.id
    LEFT JOIN
        TotalCosts tc ON s.id = tc.sale_id
    """
    if sort_by == "c.name":
        where = f"WHERE c.name ILIKE '%' || :value || '%'"
        values = {"value": string}
    elif sort_by == "s.id":

        if string != "":
            try:
                string = int(string)
                where = f"WHERE s.id = (:value)"
                values = {"value": string}
            except:
                pass
    elif sort_by == "s.address":
        where = f"WHERE s.address ILIKE '%' || :value || '%'"
        values = {"value": string}
    elif sort_by == "u.last_name":
        where = f"""WHERE u.first_name ILIKE '%' || :value || '%'
                OR u.last_name ILIKE '%' || :value || '%'"""
        values = {"value": string}

    end = f" ORDER BY {sort_by + asc_or_desc};"

    sql += where + end
    result = query_wrap(sql, values)
    return result.fetchall()

def order_details_by_id(order_id):
    sql = """
    SELECT
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
    """
    values = {"order_id":order_id}
    result = query_wrap(sql, values)
    return result.fetchone()

def products_in_order(order_id):
    sql = """
    SELECT
        p.name AS product_name,
        sd.quantity
    FROM
        Salesdetail sd
    INNER JOIN
        Products p ON sd.product_id = p.id
    WHERE
        sd.order_id = :order_id;
    """
    values = {"order_id":order_id}
    result = query_wrap(sql, values)
    return result.fetchall()

def sum_total():
    sql = """
    SELECT
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
    """
    result = query_wrap(sql, None)
    return result.fetchall()

#Sales

def sum_sales():
    sql = """
    SELECT COUNT(*) AS total_sales, SUM(total_amount) AS total_revenue
    FROM Sales;
    """
    result = query_wrap(sql, None)
    return result.fetchall()

#customer

def find_customer(customer):
    sql = "SELECT * FROM Customers WHERE LOWER(name)=LOWER((:customer))"
    values = {"customer": customer}
    result = query_wrap(sql, values)
    return result.fetchone()
