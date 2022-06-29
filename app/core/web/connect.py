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

import random



# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.database_connection import Database

from admin.admins import Admin

from date import date_now


# IMPORTS FLASK
from flask import Blueprint, render_template, abort, request, redirect, session



connect = Blueprint(
    "connect", 
    __name__
)



@connect.route("/", methods=["POST", "GET"])
def page_connect():

    if session.get("admin", None) != None:

        if request.method == "POST":

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
                api_key,
                user_group
            )
            VALUES
            (
                '{request.json["name"]}',
                '{request.json["description"]}',
                '{new_key}',
                '{request.json["user-group"]}'
            )
            """)

            db.close()


            return redirect("/connected-apps")


        else:

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            SELECT
            connected_apps.name, 
            connected_apps.description, 
            connected_apps.api_key, 
            connected_apps.id,

            user_groups.name

            FROM
            connected_apps
            INNER JOIN
            user_groups
            ON user_groups.id = connected_apps.user_group
            """)
            data = db.cursor.fetchall()

            db.cursor.execute("""
            SELECT
            id, name
            FROM
            user_groups
            """)
            user_groups = db.cursor.fetchall()


            return render_template("connected-apps.html", admin=session["admin"], data=data, user_groups=user_groups)


    else:
        return redirect("/login")






@connect.route("/delete")
def page_connect_delete():

    if session.get("admin", None) != None:

        if request.args.get("id", None) != None:

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            DELETE
            FROM
            connected_apps
            WHERE
            id = '{request.args["id"]}'
            """)

            db.close()

            return redirect("/connected-apps")

        else:
            return abort(400)

    else:
        return redirect("/login")








# THIS IS THE API ENDPOINT FOR THE REQUESTS OF YOUR EXTERNAL APPS
@connect.route("/register", methods=["POST"])
def page_connect_register():

    firstname = request.form.get("firstname", None)
    surname = request.form.get("surname", None)
    email = request.form.get("email", None)
    api_key = request.headers.get("Token", None)

    print(request.form)
    print(request.headers)

    print(firstname, surname, email, api_key)

    print("ok")

    if firstname != None and surname != None and email != None and api_key != None:

        print("ok1")

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        SELECT
        user_group
        FROM
        connected_apps
        WHERE
        api_key = '{api_key}'
        """)

        user_group = db.cursor.fetchall()[0][0]

        if user_group != []:

            print("ok2")

            db.cursor.execute(f"""
            SELECT
            users.email,
            users_in_groups.user_id
            
            FROM users
            INNER JOIN users_in_groups
            ON users_in_groups.user_id = users.id

            WHERE
            users_in_groups.group_id = '{user_group}'
            AND
            users.email = '{email}'
            """)

            query = db.cursor.fetchall()
            

            print(query)

            if query == []:

                print("ok3")
                
                db.cursor.execute(f"""
                INSERT INTO
                users
                (
                    firstname,
                    surname,
                    email,
                    since
                )
                VALUES
                (
                    '{firstname}',
                    '{surname}',
                    '{email}',
                    '{date_now()}'
                )
                """)

                db.cursor.execute(f"""
                SELECT
                id
                FROM
                users
                WHERE
                email = '{email}'
                """)

                id = db.cursor.fetchall()[0][0]

                db.cursor.execute(f"""
                INSERT INTO
                users_in_groups
                (
                    group_id,
                    user_id
                )
                VALUES
                (
                    '{user_group}',
                    '{id}'
                )
                """)
            
                db.close()

                print("ok4")

                return "Ok!"

            return "User already exists in this group!"

            

        else:
            return "Invalid token!"
        



    else:
        return "You need to fill out all the necesary payload!"