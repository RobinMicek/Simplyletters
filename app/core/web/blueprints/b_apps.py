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
import random

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
b_apps = Blueprint(
    "connected_apps", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_apps.route("/connect-apps", methods=["POST", "GET"])
@required_level_two
def page_apps():
    
    if request.method != "POST":

        return render_template("connect-apps.html",
        apps = Queries().query_apps(),
        user_groups = Queries().query_user_groups(),
        username = session["account"])

    else:

        new_key = "simplyletters./"
        string = "QWERTZUIOPASDFGHJKLYXCVBNMqwertzuiopasdfghjklyxcvbnm"
        for x in range(16):
            new_key += string[random.randrange(1,15)]

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        INSERT INTO
        connected_apps
        (
            name,
            description,
            user_group,
            api_key
        )
        VALUES
        (
            "{request.form.get("name").replace('"', "'")}",
            "{request.form.get("description").replace('"', "'")}",
            "{request.form.get("user-group")}",
            "{new_key}"
        )
        """)
        db.close()

        return redirect("/connect-apps")


@b_apps.route("/connect-app/delete")
@required_level_two
def page_admin_delete():

    db = Database()
    db.connect()
    db.cursor.execute(f"""
    DELETE
    
    FROM connected_apps

    WHERE id = "{request.args.get('id', None)}"
    """)
    db.close()

    return redirect("/connect-apps")