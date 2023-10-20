from db import db
from sqlalchemy.sql import text
from query import find_customer, product_query
from customer import new_customer

def add_order_to_database(customer, address, product_id, quantity, sales_person_id):
    try:
        
        if not find_customer(customer):
            new_customer(customer, address)
        customer_id = find_customer(customer)[0]
        product = product_query(product_id)

        total_amount = product[4] * quantity

        sql = text("""INSERT INTO Sales (customer_id, sale_date, address, sales_person_id, total_amount)
                VALUES (:customer_id, NOW(), :address, :sales_person_id, :total_amount) 
                RETURNING id
        """)
        
        result = db.session.execute(sql, {
            "customer_id":customer_id,
            "address":address,
            "sales_person_id":sales_person_id,
            "total_amount": total_amount})
        db.session.commit()
        
        id = result.fetchone()[0]

        if id:

            sql = text("""
                INSERT INTO Salesdetail (order_id, product_id, quantity)
                VALUES (:order_id, :product_id, :quantity) RETURNING id
            """)
            db.session.execute(sql, {"order_id":id, "product_id":product_id, "quantity":quantity})
            db.session.commit()
        
        return id
    
    except:
        db.session.rollback()

def modify_order_add_product(order_id, product_id, quantity):
        try:
            sql = text("""
                    INSERT INTO Salesdetail (order_id, product_id, quantity)
                    VALUES (:order_id, :product_id, :quantity) 
                    RETURNING id
            """)
            db.session.execute(sql, {"order_id":order_id, "product_id":product_id, "quantity":quantity})
            db.session.commit()
        except:
            db.session.rollback()