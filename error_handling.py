from app import app
from db import db
from sqlalchemy.sql import text
from flask import render_template, request

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def server_error(e): 
    return render_template("500.html", message=e)

def query_wrap(sql, values):
    try:
        result = db.session.execute(text(sql), values)
    except Exception as e:
        print("error in query: ", e)
        result = None
    return result