from db import db
from sqlalchemy.sql import text
from query import find_customer, product_query, check_product_in_salesdetail, product_quantity_in_warehouse
import query as q
from customer import new_customer

def add_order_to_database(customer, address, product_id, quantity, sales_person_id):
    try:
        if not find_customer(customer):
            new_customer(customer, address)

        customer_id = find_customer(customer)[0]
        product = product_query(product_id)
        total_amount = product[4] * quantity

        collect_items_from_warehouses(product_id, quantity)
        
        sql = text("""
                INSERT INTO Sales (customer_id, sale_date, address, sales_person_id, total_amount)
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
    
    except Exception as e:
        print(e)
        db.session.rollback()

def modify_order_add_product(order_id, product_id, quantity):

        product_already_in = check_product_in_salesdetail(product_id, order_id)

        product = q.product_query(product_id)
        add_to_total = product.price * quantity

        if product_already_in != None:

            quantity_in_order = product_already_in[0]
            new_quantity = quantity_in_order + quantity
            sql = text("""
                UPDATE Salesdetail 
                SET quantity = (:new_quantity) 
                WHERE order_id = (:order_id) AND product_id = (:product_id)
                """)
            
            values = {"order_id": order_id, "product_id": product_id, "new_quantity": new_quantity}
        else:
            sql = text("""
                    INSERT INTO Salesdetail (order_id, product_id, quantity)
                    VALUES (:order_id, :product_id, :quantity) 
                    RETURNING id
            """)
            values = {"order_id":order_id, "product_id":product_id, "quantity":quantity, "add_to_total": add_total}
        try:
            db.session.execute(sql, values)
            db.session.commit()
            change_order_total(order_id, add_to_total)
        except Exception as e:
            db.session.rollback()
            print(e)

def change_order_total(order_id, add_to_total):
    total = q.get_order(order_id).total_amount
    total += add_to_total
    sql = text("""
            UPDATE Sales 
            SET total_amount = (:total) 
            WHERE id = (:order_id)
            """)
    
    try:
        db.session.execute(sql, {"order_id": order_id, "total": total})
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(e)


def remove_items_from_warehouse(product_id, warehouse_id, quantity):
    quantity_in_warehouse = product_quantity_in_warehouse(product_id, warehouse_id)
    
    new_quantity = quantity_in_warehouse[0] - quantity
    sql = text("""
        UPDATE Inventory_item
        SET unit_size = (:new_quantity) 
        WHERE product_id = (:product_id) AND location_id = (:warehouse_id)
    """)
    values = {"product_id":product_id, "warehouse_id": warehouse_id, "new_quantity": new_quantity}
    
    try:
        db.session.execute(sql, values)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

def collect_items_from_warehouses(product_id, quantity):
    inventory = q.count_product_per_warehouse(product_id)

    for warehouse in inventory:
        
        if quantity == 0: break

        warehouse_id = warehouse[0]
        quantity_in_wh = warehouse[2]
        
        if quantity_in_wh >= quantity:
            remove_items_from_warehouse(product_id, warehouse_id, quantity)
            quantity = 0
        
        else:
            remove_items_from_warehouse(product_id, warehouse_id, quantity_in_wh)          
            quantity -= quantity_in_wh