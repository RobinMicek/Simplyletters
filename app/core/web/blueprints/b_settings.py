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

from variables import FLASK_SECRET_KEY


# INICIALIZE BLUEPRINT
b_settings = Blueprint(
    "settings", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_settings.route("/settings", methods=["POST", "GET"])
@required_level_two
def page_settings():
    
    if request.method != "POST":

        return render_template("settings.html",
        settings = Queries().query_settings(),
        username = session["account"])

    else:

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        UPDATE
        newsletters_config

        SET 
        logo = "{request.form.get("logo", None).replace('"', "'")}",
        footer = "{request.form.get("footer", None).replace('"', "'")}"
        """)
        db.close()

        return redirect("/settings")