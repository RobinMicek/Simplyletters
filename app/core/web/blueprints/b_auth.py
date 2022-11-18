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

from auth.auth import Admin
from auth.auth_wrappers import required_level_one

from variables import FLASK_SECRET_KEY


# INICIALIZE BLUEPRINT
b_auth = Blueprint(
    "auth", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_auth.route("/login", methods=["POST", "GET"])
def page_login():

    if request.method != "POST":

        return render_template("login.html")

    else:
        username = request.form["username"].replace("'", "").replace('"', '')
        password = request.form["password"].replace("'", "").replace('"', '')

        user = Admin(username = username)

        if user.auth(password = password) == True:
            
            # Add session variable
            session["account"] = username
            session["level"] = user.get_level()

            return redirect("/")

        else:
            return render_template("login.html")


@b_auth.route("/logout")
@required_level_one
def page_logout():

    session.pop("account")
    session.pop("level")

    return redirect("/login")
