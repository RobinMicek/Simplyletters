"""
******************************************

    This code is part of SimplyLetters

    github.com/RobinMicek/SimplyLetters

------------------------------------------   

    written by Robin Míček

    released under MIT License

******************************************
"""
# IMPORTS
import sys
import os

# IMPORTS FROM PACKAGES
from flask import Blueprint, render_template, abort, request, redirect, session

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from queries.queries import Queries

from database.handle_database import Database

from auth.auth import Admin

from variables import FLASK_SECRET_KEY


# INICIALIZE BLUEPRINT
b_fts = Blueprint(
    "first time setup", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_fts.route("/fts", methods=["POST", "GET"])
def page_fts():

    if Queries().query_check_fts() == False:

        if request.method != "POST":
            
            return render_template("fts.html")


        else:
            
            db = Database()

            # Inicialize Database
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
                "{request.form["company_name"]}",
                "{request.form["description"]}"

            )
            """)

            db.cursor.execute(f"""
            INSERT INTO
            email_credentials
            (
                smtp_server,
                email,
                password
            )
            VALUES
            (
                "{request.form["smtp_server"]}",
                "{request.form["smtp_email"]}",
                "{request.form["smtp_password"]}"
            )
            """)
            db.close()

            new_admin = Admin(username=request.form["username"])
            new_admin.create_admin(password=request.form["password"], level="2")

            return redirect("/")
    else:

        return redirect("/")
