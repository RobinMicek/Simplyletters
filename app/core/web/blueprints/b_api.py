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

from auth.auth_wrappers import required_level_one, required_level_two, required_level_api

from database.handle_database import Database

from queries.queries import Queries

from newsletter.handle_newsletter import Newsletter

from auth.auth import Admin

from date import date_now

from variables import FLASK_SECRET_KEY


# INICIALIZE BLUEPRINT
b_api = Blueprint(
    "api", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_api.route("/connect-app/register", methods=["POST"])
def page_api_connect():

    firstname = request.json.get("firstname", None)
    surname = request.json.get("surname", None)
    email = request.json.get("email", None)
    api_key = request.headers.get("Token", None)

    if firstname != None and surname != None and email != None and api_key != None:

        
        firstname = firstname.replace('"', "").replace("'", "")
        surname = surname.replace('"', "").replace("'", "")
        email = email.replace('"', "").replace("'", "")
        api_key = api_key.replace('"', "").replace("'", "")


        db = Database()
        db.connect()
        db.cursor.execute(f"""
        INSERT IGNORE INTO users 
        (
            firstname,
            surname,
            email,
            since
        )

        VALUES
        (
            "{firstname}",
            "{surname}",
            "{email}",
            "{date_now()}"
        )
        """)

        db.cursor.execute(f"""
        SET @user_id := (
            SELECT id
            
            FROM users
                
            WHERE users.email = "{email}"
            
            LIMIT 1
        )
        """)

        db.cursor.execute(f"""
        SET @group_id := (
            SELECT user_group 
            
            FROM connected_apps 
                
            WHERE connected_apps.api_key  = "{api_key}"
        )
        """)
        
        db.cursor.execute(f"""
        INSERT INTO users_in_groups 
        (
            user_id,
            group_id
        )

        VALUES
        (
            @user_id,
            @group_id
        )
        """)
    
        db.close()

        return "OK!"

    return abort(400)


@b_api.route("/api/create-newsletter", methods=["POST"])
def page_api_create_newsletter():


    auth_user = request.headers.get("user", None)
    auth_password = request.headers.get("password", None)

    if auth_user != None and auth_password != None:

        auth_user = auth_user.replace('"', "").replace("'", "")
        auth_password = auth_password.replace('"', "").replace("'", "")

        user = Admin(username=auth_user)

        if user.auth(password = auth_password) and int(user.get_level()) == 3:

            newsletter_info = request.json.get("newsletter", None)
            newsletter_content = newsletter_info.get("content", None)

            if newsletter_info != None and newsletter_content != None:

                # Get footer and logo
                db = Database()
                db.connect()
                db.cursor.execute("""
                SELECT
                logo, 
                footer

                FROM newsletters_config
                """)
                query = db.cursor.fetchall()
                db.close()

                newsletter_content["logo"] = query[0]["logo"]
                newsletter_content["footer"] = query[0]["footer"]
 
                try:

                    newsletter = Newsletter(**newsletter_content)

                    id = newsletter.create_newsletter(admin = user.username)

                    if newsletter_info["info"]["send_group"] == "true":

                        newsletter.send_email(
                            id = id,
                            group = True
                        )

                        return "OK!"

                    elif newsletter_info["info"]["send_group"] == "false":

                        newsletter.send_email(
                            id = id,
                            group = False,
                            email = newsletter_info["info"]["email"]
                        )

                        return "OK!"

                    return abort(400)

                except:

                    return abort(400)

                    