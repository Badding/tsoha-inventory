from db import db
from sqlalchemy.sql import text
import query as q

def add_inventory_to_warehouse(product_id, warehouse_id, supplier_id, quantity):    
    in_warehouse = q.product_quantity_in_warehouse(product_id, warehouse_id)

    values = {
        "product_id":product_id,
        "unit_size":quantity,
        "supplier_id":supplier_id,
        "warehouse_id":warehouse_id
        }
    
    if in_warehouse == None:
        sql = text("""
            INSERT INTO Inventory_item (product_id, unit_size, supplier_id, location_id) 
            VALUES (:product_id, :unit_size, :supplier_id, :warehouse_id)
            """)
    else:
        sql = text("""
            UPDATE Inventory_item
            SET unit_size = (:unit_size) 
            WHERE product_id = (:product_id) AND location_id = (:warehouse_id)
            """)
        
        try:
            
            values["unit_size"] = int(in_warehouse[0]) + int(quantity),
            
        except:
            pass
    
    try:
        db.session.execute(sql, values)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    