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

import json

# IMPORTS FROM PACKAGES
from flask import Blueprint, render_template, abort, request, redirect, session

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from auth.auth_wrappers import required_level_one, required_level_two

from database.handle_database import Database

from queries.queries import Queries

from auth.auth import Admin

from variables import FLASK_SECRET_KEY


# INICIALIZE BLUEPRINT
b_admins = Blueprint(
    "admins", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_admins.route("/admins", methods=["POST", "GET"])
@required_level_two
def page_admins():
    
    if request.method != "POST":

        return render_template("admins.html",
        admins = Queries().query_admins(),
        username = session["account"])

    else:

        admin = Admin(username = request.form.get("username", None))
        admin.create_admin(password = request.form.get("password", None), level = request.form.get("level", None))

        return redirect("/admins")


@b_admins.route("/admin/delete")
@required_level_two
def page_admin_delete():

    db = Database()
    db.connect()
    db.cursor.execute(f"""
    DELETE
    
    FROM admins

    WHERE id = "{request.args.get('id', None)}"
    """)
    db.close()

    return redirect("/admins")