from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def new_user(username, password, access_level):
    try:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password, access_level) VALUES (:username, :password, :access_level)")
        db.session.execute(sql, {"username":username, "password":hash_value, "access_level":access_level})
        db.session.commit()
    except:
        print("create user failed")

def check_user_password(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    result = False
    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            result = True
    return result