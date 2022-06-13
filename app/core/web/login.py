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
# LOGIN

# IMPORTS
import sys
import os



# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.database_connection import Database

from admin.admins import Admin

# IMPORTS FLASK
from flask import Blueprint, render_template, abort, request, redirect, session



login = Blueprint(
    "login", 
    __name__,
    template_folder='templates_login'
)


@login.route("/", methods=["GET", "POST"])
def page_login():

    if request.method == "POST":
        
        admin = Admin(str(request.form["username"]))

        if admin.auth(str(request.form["password"])) == True:
            
            session["admin"] = str(request.form["username"])

            return redirect("/")
        else:
            return render_template("login.html")

    else:
        if session.get("admin", None) == None:
            return render_template("login.html")

        else:
            return redirect("/")


@login.route("/logout")
def page_login_logout():

    if session.get("admin", None) == None:
        return redirect("/login")

    else:
        session.pop("admin")
        return redirect("/login")