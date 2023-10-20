from db import db
from sqlalchemy.sql import text

def new_product(product):
    try:
            
            p = product["product"]
            m = product["manufacturer"]
            d = product["description"]
            n = product["price"]
            n = round(float(n), 2)
            n = "{:.2f}".format(n)        
            pr = int((float(n)) * 100)
            
            print(p,m,d,pr)
            sql = text("""
                    INSERT INTO Products (name, manufacturer, description, price) 
                    VALUES (:name, :manufacturer, :description, :price)
                    """)

            db.session.execute(sql,{"name":p, "manufacturer":m, "description":d, "price":pr})
            db.session.commit()

    except:
        db.session.rollback()
