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
# DASHBOARD

# IMPORTS
import sys
import os



# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.database_connection import Database

from admin.admins import Admin

from emailing.create_email import Email_Template


# IMPORTS FLASK
from flask import Blueprint, render_template, abort, request, redirect, session



api = Blueprint(
    "api",
    __name__
)



@api.route("/create-newsletter", methods=["POST"])
def api_create_user():

    auth_user = request.headers.get("user", None)
    auth_password = request.headers.get("password", None)

    print("Request has been made!")

    if auth_user != None and auth_password != None:

        user = Admin(auth_user)
        
        if user.auth(auth_password) == False:

            print("Wrong user!")

            return "Wrong user!"

        else:

            try:
                # Get footer and logo
                db = Database()
                db.connect()
                db.cursor.execute("""
                SELECT
                logo,
                footer 
                
                FROM newsletters_config
                """)

                x = db.cursor.fetchall()[0]

                logo = x[0]
                footer = x[1]


                # Get id of "user_group" for REST API newsletters
                db.cursor.execute("""
                SELECT
                id

                FROM user_groups

                WHERE name = "API"
                """)
                user_group = db.cursor.fetchall()[0][0]

                db.close()


                newsletter = Email_Template(
                    request.json["template-number"],
                    request.json["color-main"],
                    request.json["color-accent"],
                    request.json["color-text"],
                    logo,
                    "",
                    footer,
                    request.json["title"],
                    request.json["perex"],
                    request.json["perex-header"],
                    [request.json["paragraphs"]],
                    request.json["slug"],
                    user_group
                )

                newsletter.create_newsletter(auth_user)

                newsletter.send_one_email(request.json["email"])

                print("Ok!")

                return "Ok!"
        
            except:

                print("Something went wrong!")

                return "Something went wrong!"