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

from newsletter.handle_newsletter import Newsletter

from variables import FLASK_SECRET_KEY


# INICIALIZE BLUEPRINT
b_groups = Blueprint(
    "groups", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_groups.route("/groups", methods=["POST", "GET"])
@required_level_one
def page_groups():

    if request.method != "POST":

        return render_template("groups.html",
        user_groups = Queries().query_user_groups(),
        username = session["account"])

    else:

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        INSERT INTO
        user_groups

        (
            name,
            description 
        )
        VALUES
        (
            "{request.form.get("name").replace('"', "'")}",
            "{request.form.get("description").replace('"', "'")}"
        )
        """)
        db.close()

        return redirect("/groups")

@b_groups.route("/group/delete")
@required_level_two
def page_group_delete():

    db = Database()
    db.connect()
    db.cursor.execute(f"""
    DELETE

    FROM user_groups

    WHERE id = "{request.args.get('id', None)}"
    """)
    db.close()

    return redirect("/groups")