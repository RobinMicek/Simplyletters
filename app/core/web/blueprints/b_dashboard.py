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

from auth.auth_wrappers import required_level_one

from queries.queries import Queries

from variables import FLASK_SECRET_KEY


# INICIALIZE BLUEPRINT
b_dashboard = Blueprint(
    "dashboard", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_dashboard.route("/")
@required_level_one
def page_dashboard():

    return render_template("index.html",
    no_of_users = Queries().query_number_of_users(),
    no_of_newsletters = Queries().query_number_of_newsletters(),
    last_created = Queries().query_last_created_newsletter(),
    most_active = Queries().query_most_active_admin(),
    company_info = Queries().query_company_info(),
    username = session["account"])
