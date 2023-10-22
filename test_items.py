from app import app
from random import randint, choice
from db import db, text
import query as q
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from users import new_user
from customer import new_customer
from orders import add_order_to_database, modify_order_add_product
from error_handling import query_wrap
"""
Reset the DB with these commands in terminal:
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

venv enviroment:
psql < schema.sql
"""

product_list = [
    "Smartphone",
    "Laptop",
    "Tablet",
    "Headphones",
    "Digital Camera",
    "Fitness Tracker",
    "Coffee Maker",
    "Blender",
    "Toaster",
    "Microwave Oven",
    "Refrigerator",
    "Washing Machine",
    "Dishwasher",
    "Television",
    "Gaming Console",
    "Monitor",
    "Printer",
    "Desk Chair",
    "Desk",
    "Office Lamp",
    "Backpack",
    "Hiking Boots",
    "Tennis Shoes",
    "Running Shoes",
    "Sunglasses",
    "Umbrella",
    "Wallet",
    "Watch",
    "Necktie",
    "Belt",
    "Dress Shirt",
    "T-Shirt",
    "Jeans",
    "Shorts",
    "Sweater",
    "Winter Coat",
    "Scarf",
    "Gloves",
    "Hat",
    "Handbag",
    "Earrings",
    "Bracelet",
    "Ring",
    "Necklace",
    "Makeup Kit",
    "Perfume",
    "Shampoo",
    "Conditioner",
    "Toothbrush",
    "Toothpaste",
    "Soap",
    "Shower Gel",
    "Towel Set",
    "Bed Sheets",
    "Pillow",
    "Blanket",
    "Curtains",
    "Dining Table",
    "Dining Chairs",
    "Sofa",
    "Coffee Table",
    "Bookshelf",
    "Bed Frame",
    "Mattress",
    "Nightstand",
    "Dresser",
    "Cookware Set",
    "Knife Set",
    "Cooking Utensils",
    "Bakeware",
    "Cutting Board",
    "Food Processor",
    "Coffee Grinder",
    "Tea Kettle",
    "Dining Plates",
    "Flatware Set",
    "Wine Glasses",
    "Coffee Mugs",
    "Kitchen Scale",
    "Cleaning Supplies",
    "Trash Can",
    "Broom",
    "Vacuum Cleaner",
    "Toolbox",
    "Power Drill",
    "Screwdriver Set",
    "Paintbrushes",
    "Hammer",
    "Lawn Mower",
    "Garden Hose",
    "Plant Pots",
    "BBQ Grill",
    "Outdoor Chairs",
    "Patio Umbrella",
    "Swimming Pool",
    "Basketball Hoop",
    "Tennis Racket",
    "Bicycle",
    "Skateboard",
    "Fishing Rod",
    "Tent",
    "Sleeping Bag",
]

finnish_addresses = [
    "Kalevankatu 12, Helsinki, 00100",
    "Mannerheimintie 42, Tampere, 33100",
    "Esplanadi 5, Turku, 20100",
    "Keskuskatu 8, Oulu, 90100",
    "Kirkkokatu 15, Jyväskylä, 40100",
    "Rautatienkatu 22, Kuopio, 70100",
    "Läntinen Pitkäkatu 17, Vaasa, 65100",
    "Hämeenkatu 10, Lahti, 15100",
    "Koulukatu 3, Joensuu, 80100",
    "Mannerheimintie 18, Rovaniemi, 96100",
    "Asemakatu 5, Seinäjoki, 60100",
    "Savontie 7, Mikkeli, 50100",
    "Kirkkokatu 12, Pori, 28100",
    "Rantakatu 2, Kotka, 48100",
    "Kauppakatu 9, Kouvola, 45100",
    "Kirkkokatu 6, Hämeenlinna, 13100",
    "Linnankatu 3, Lappeenranta, 53100",
    "Pohjoinen Rautatiekatu 14, Kajaani, 87100",
    "Kauppatori 1, Raisio, 21200",
    "Kuuselankatu 4, Nurmijärvi, 01900",
    "Metsälänkatu 11, Kerava, 04200",
    "Kaivokatu 5, Kokkola, 67100",
    "Kauppakatu 2, Imatra, 55100",
    "Hakakatu 8, Paimio, 21500",
    "Satamakatu 1, Naantali, 21100",
]

customers = [
    "Wernham Hogg Paper Company",
    "Vance Refrigeration",
    "WUPHF.com",
    "Utica Paper",
    "Prince Family Paper",
    "Saticoy Steel",
    "City of Scranton",
    "Serenity by Jan",
    "Alfredo's Pizza Cafe",
    "Hammermill Paper Company",
    "Scranton White Pages",
]

warehouses = ["Helsinki", "Oulu", "Rovaniemi", "Jyväskylä"]
categories = [""]
manufacturer = ["Lamasonic", "Phony", "Mokia", "Sumsang", "BG"]
suppliers = ["Bestdeals", "Lamazon", "hokmanni"]
users = [
    ("michael", "Michael", "Scott", "manager", "manager"),
    ("admin", "Ryan", "Howard", "admin", "admin"),
    ("jim", "Jim", "Halpert", "sales", "sales"),
    ("pam", "Pam", "Beesly", "sales", "sales"),
    ("andy", "Andy", "Bernard", "sales", "sales"),
    ("stanley", "Stanley", "Hudson", "sales", "sales"),
    ("sales", "Sale", "Person", "sales", "sales"),
    ("manager", "Manager", "Person", "manager", "manager")
]

#fill warehouse table
def create_test_warehouses():
    failed = False
    for wh in warehouses:
        try:
            if q.find_warehouse(wh): 
                continue

            sql = text("INSERT INTO warehouses (name) VALUES (:name)")
            db.session.execute(sql,{"name":wh} )
            db.session.commit()
        except:
            failed = True
            break
    if failed: print("Warehouse table creation failed")
    else: print("Warehouse table filled")
    
#fill suppliers table
def create_test_suppliers():
    failed = False
    for m in suppliers:
        try: 

            if q.find_supplier(m):
                continue

            addr = choice(finnish_addresses)
            sql = text("INSERT INTO suppliers (name, address) VALUES (:name, :address)")
            db.session.execute(sql,{"name":m, "address":addr})
            db.session.commit()
        except:
            failed = True
            break
    if failed: print("Suppliers table creation failed")
    else: print("Suppliers table filled")

#generates 100 products for the database
def create_test_products():
    failed = False
    for product in product_list:
        try:
            #if q.product_by_name(product):
            #    continue

            n = product
            m = choice(manufacturer)
            d = "this is a sample description for product: " + product
            pr = randint(50, 5000)

            sql = text("INSERT INTO Products (name, manufacturer, description, price) VALUES (:name, :manufacturer, :description, :price)")

            db.session.execute(sql,{"name":n, "manufacturer":m, "description":d, "price":pr})
            db.session.commit()
            
        except:
            failed = True
            break
    if failed: print("Products table creation failed")
    else: print("products created")

def fill_warehouses():
    failed = False
    
    for p in product_list:

            p_id = q.product_by_name(p)
            s = choice(suppliers)
            s_id = q.find_supplier(s)

            for warehouse in warehouses:
                u = randint(0,5) * 10
                wh_id = q.find_warehouse(warehouse)
                if p_id == None or wh_id == None or s_id == None:
                    continue

                try:
                    
                    sql = text("""INSERT INTO Inventory_item (product_id, unit_size, supplier_id, location_id) 
                            VALUES (:product_id, :unit_size, :supplier_id, :location_id)""")
                    db.session.execute(sql,{"product_id":p_id[0], "unit_size":u, "supplier_id":s_id[0], "location_id":wh_id[0]})
                    db.session.commit()
                except:
                    failed = True
                    db.session.rollback()
                    break
            """

            for unit in range(units_created):
                u = unit_size
                p_id = q.product_by_name(p)
                s = choice(suppliers)
                s_id = q.find_supplier(s)
                w = choice(warehouses)
                wh_id = q.find_warehouse(w)
            """

    if failed: print("failed to fill warehouses")
    else: print("warehouse filled")

def create_users():
    for user in users:
        try:
            #if q.user_exists(user): continue

            username, first, last, password, position = user
            new_user(username, first, last, password, position)
        except:
            pass

def create_customers():
    for i in range(len(customers)):
        try:
            #if q.find_customer(customer[i]): continue

            customer = customers[i]
            address = finnish_addresses[i]        
            new_customer(customer, address)
        except:
            pass

def create_sales():
    sales = 20
    failed = False
    
    for i in range(sales):
        try:
            c = choice(customers)
            address = q.find_customer(c)[2]
            p = choice(product_list)
            p_id = q.product_by_name(p)[0]
            quantity = randint(5,50) * 10
            seller = q.user_exists(choice(users)[0])[0]
            last_order = add_order_to_database(c, address, p_id, quantity, seller)
            product_in_order = randint (2,6)
            for j in range(product_in_order):
                p = choice(product_list)
                p_id = q.product_by_name(p)[0]
                quantity = randint(5,50) * 10
                
                modify_order_add_product(last_order, p_id, quantity)
        except Exception as error:
            failed = True
    if failed: print("failed to fill sales: ")
    else: print("sales filled")

def create_test_db():
    """
    """
    create_users()
    create_test_warehouses()
    create_test_suppliers()
    create_test_products()
    fill_warehouses()
    create_customers()
    create_sales()
    #test_error_handling()