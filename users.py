from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from error_handling import query_wrap
from db import db

def new_user(username, first, last, password, position):
    try:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, first_name, last_name, password, position) VALUES (:username, :first_name, :last_name, :password, :position)")
        db.session.execute(sql, {"username":username, "first_name":first, "last_name":last, "password":hash_value, "position":position})
        db.session.commit()
    except:
        db.session.rollback()

def remove_user(id):
    try:
        sql = text("DELETE FROM Users WHERE id=:id")
        db.session.execute(sql,{"id":id})
        db.session.commit()
    except:
        db.session.rollback()


def check_user_password(username, password):
    #sql = text("SELECT id, password FROM users WHERE username=:username")
    #result = db.session.execute(sql, {"username":username})
    #user = result.fetchone()

    sql = "SELECT id, password FROM users WHERE username=:username"
    values = {"username": username, "password": password}
    result = query_wrap(sql, values)
    user = result.fetchone()

    result = False
    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            result = True
    return result
