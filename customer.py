from sqlalchemy.sql import text
from db import db

def new_customer(customer, address):
    try:
        sql = text("""INSERT INTO Customers (name, address)
                VALUES (:name, :address)
                """)
        db.session.execute(sql, {"name":customer, "address":address})
        db.session.commit()
    
    except:
        db.session.callback()