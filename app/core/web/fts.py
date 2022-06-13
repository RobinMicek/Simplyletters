"""
******************************************
    
    ABOUT THIS CODE

------------------------------------------ 

    This code is part of SimplyLetters

    github.com/RobinMicek/SimplyLetters

------------------------------------------   

    written by Robin Míček

    released under MIT License

******************************************
"""


# THIS IS A FLASK BLUEPRINT
# FIRST TIME SETUP

# IMPORTS
import sys
import os

from time import sleep


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.database_connection import Database

from admin.admins import Admin

# IMPORTS FLASK
from flask import Blueprint, render_template, abort, request, redirect



fts = Blueprint(
    "fts", 
    __name__,
    template_folder='templates_fts'
)




@fts.route("/")
def page_fts_index():

    db = Database()
    db.connect()
    db.cursor.execute("""
    SHOW TABLES
    """)
    query = db.cursor.fetchall()

    print(query)

    if query == []:

        return render_template("fts.html")

    else:
        return redirect("/")


@fts.route("/make", methods=["POST"])
def page_fts_make():

    db = Database()
    db.connect()
    db.cursor.execute("""
    SHOW TABLES
    """)
    query = db.cursor.fetchall()
    db.close()

    print(query)

    if query == []:

        
        db.initialize()
        db.connect()
        db.cursor.execute(f"""
        INSERT INTO
        config
        (
            company_name,
            description
        )
        VALUES
        (
            '{request.form["newsletter-name"]}',
            '{request.form["description"]}'
        )
        """)

        db.cursor.execute(f"""
        INSERT INTO
        email_credentials
        (
            email,
            password,
            smtp_server
        )
        VALUES
        (
            '{request.form["email"]}',
            '{request.form["password"]}',
            '{request.form["smtp"]}'
        )
        """)

        db.db.commit()

        new_admin = Admin(str(request.form["admin-username"]))

        new_admin.create_admin(str(request.form["admin-password"]), 2)


        
        return redirect("/")


    else:
        return redirect("/")