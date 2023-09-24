from app import app
from random import randint, choice
from db import db, text
from query import find_warehouse, find_supplier, product_by_name
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
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

warehouses = ["Helsinki", "Oulu", "Rovaniemi", "Jyväskylä"]
categories = [""]
manufacturer = ["Lamasonic", "Phony", "Mokia", "Sumsang", "BG"]
suppliers = ["Bestdeals", "Lamazon", "hokmanni"]

#fill warehouse table
def create_test_warehouses():
    failed = False
    for wh in warehouses:
        try:
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
            n = product
            m = choice(manufacturer)
            d = "this is a sample description for product: " + product
            pr = randint(50, 5000000)

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
        try:
            q = randint(1, 250)
            p_id = product_by_name(p)
            s = choice(suppliers)
            s_id = find_supplier(s)
            w = choice(warehouses)
            wh_id = find_warehouse(w)

            sql = text("INSERT INTO Inventory_item (product_id, quantity, supplier_id, location_id) VALUES (:product_id, :quantity, :supplier_id, :location_id)")
            db.session.execute(sql,{"product_id":p_id, "quantity":q, "supplier_id":s_id, "location_id":wh_id})
            db.session.commit()
        except:
            failed = True
            break
    if failed: print("failed to fill warehouses")
    else: print("warehouse filled")

def create_test_db():
    create_test_warehouses()
    create_test_suppliers()
    create_test_products()
    fill_warehouses()

def test_list(list):
    seen = []
    for item in list:
        if item not in seen:
            seen.append(item)
        else:
            print("item dublicate: " + item)