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
from types import new_class



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
                print(request.form)

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
                
                print(logo, footer)

                paragraphs = [{
                        "image": "https://helpx.adobe.com/content/dam/help/en/photoshop/using/convert-color-image-black-white/jcr_content/main-pars/before_and_after/image-before/Landscape-Color.jpg",
                        "header": "Funguje to?",
                        "text": "Tohle by snad již mohlo fungovat! Uvidíme no..."
                    },
                    {
                        "image": None,
                        "header": "Second",
                        "text": "Ipsum Lorem"
                    }]
            
                print(paragraphs)

                newsletter = Email_Template(
                    request.form["template-number"],
                    request.form["color-main"],
                    request.form["color-accent"],
                    request.form["color-text"],
                    logo,
                    "",
                    footer,
                    request.form["title"],
                    request.form["perex"],
                    request.form["perex-header"],
                    paragraphs,
                    request.form["slug"],
                    0
                )

                print("Ok!")

                print(newsletter.paragraphs)

                newsletter.create_newsletter(auth_user)

                print("Ok!")

                return "Ok!"
        
            except:

                print("Something went wrong!")

                return "Something went wrong!"