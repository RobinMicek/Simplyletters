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


# IMPORTS FLASK
from flask import Blueprint, render_template, abort, request, redirect, session



dashboard = Blueprint(
    "dashboard", 
    __name__,
    template_folder='templates'
)


@dashboard.route("/")
def page_dashboard_home():

    db = Database()
    db.connect()
    db.cursor.execute("""
    SHOW TABLES
    """)
    query = db.cursor.fetchall()

    if query == []:

        return redirect("/fts")

    else:
        if session.get("admin", None) == None:
            
            return redirect("/login")

        else:


            db.connect()
            db.cursor.execute("""
            SELECT
            COUNT(*)
            FROM
            newsletters
            """)
            a = db.cursor.fetchall()[0][0]

            db.cursor.execute("""
            SELECT
            COUNT(*)
            FROM
            users
            """)
            b = db.cursor.fetchall()[0][0]

            data = {
                "newsletters": str(a),
                "users": str(b)
            }



            return render_template("homepage.html", admin=session["admin"], data=data)



@dashboard.route("/settings", methods=["GET", "POST"])
def page_dashboard_settings():

    if request.method == "POST":
        if session.get("admin", None) == None:

            return redirect("/login")
            
        else:
            
            db = Database()
            db.connect()
            db.cursor.execute(f"""
            UPDATE
            newsletters_config
            SET
            footer = '{request.form["footer"]}',
            logo = '{request.form["logo"]}'
            """)

            db.cursor.execute(f"""
            UPDATE
            email_credentials
            SET
            email = '{request.form["email"]}',
            password = '{request.form["password"]}',
            smtp_server = '{request.form["smtp"]}'
            """)

            db.close()

            return redirect("/settings")

    else:
        if session.get("admin", None) == None:
            
            return redirect("/login")

        else:

            db = Database()
            db.connect()
            
            db.cursor.execute("""
            SELECT
            logo, footer
            FROM
            newsletters_config
            """)

            x = db.cursor.fetchall()

            db.cursor.execute("""
            SELECT
            email, password, smtp_server
            FROM
            email_credentials
            """)

            y = db.cursor.fetchall()

            db.close()

            if x != []:

                data = {
                    "logo": x[0][0],
                    "footer": x[0][1],
                    "email": y[0][0],
                    "password": y[0][1],
                    "smtp": y[0][2]
                }

            else:
                
                data = {
                    "logo": "",
                    "footer": "",
                    "email": "",
                    "password": "",
                    "smtp": ""
                }

            return render_template("settings.html", admin=session["admin"], data=data)




@dashboard.route("/groups", methods=["POST", "GET"])
def page_dashboard_groups():

    if session.get("admin", None) != None:
        
        if request.method == "POST":
            
            
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
                '{request.form["name"]}',
                '{request.form["description"]}'
            )
            """)
            db.close()

            return redirect("/groups")

        else:

            db = Database()
            db.connect()
            db.cursor.execute("""
            SELECT 
            id, name, description
            FROM 
            user_groups
            """)
            
            x = db.cursor.fetchall()

            data = []


            for y in x:

                db.cursor.execute(f"""
                SELECT
                COUNT(*)
                FROM
                users_in_groups
                WHERE
                group_id = {y[0]}
                """)
                user_count = db.cursor.fetchall()

                data += [{
                    "id": y[0],
                    "name": y[1],
                    "description": y[2],
                    "user_count": user_count
 
                }]

            
            db.close()
            

            return render_template("groups.html", admin=session["admin"], data=data)

    else:
        return redirect("/login")



        


@dashboard.route("/groups/delete")
def page_dashboard_groups_delete():

    if session.get("admin", None) != None:

        if request.args.get("id", None) != None:

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            DELETE
            FROM
            user_groups
            WHERE
            id = {request.args["id"]}
            """)

            db.cursor.execute(f"""
            DELETE
            FROM
            users_in_groups
            WHERE
            group_id = {request.args["id"]}
            """)

            db.close()

            return redirect("/groups")

        else:
            return abort(400)

    else:
        return redirect("/login")




@dashboard.route("/users")
def page_dashboard_users():

    if session.get("admin", None) != None:
        
       

        db = Database()
        db.connect()
        db.cursor.execute("""
        SELECT 
        users.firstname, 
        users.surname, 
        users.email,

        user_groups.name
        
        FROM 
        users

        INNER JOIN
        users_in_groups
        ON users.id = users_in_groups.user_id
        
        INNER JOIN
        user_groups 
        ON users_in_groups.group_id = user_groups.id 
        """)
        
        x = db.cursor.fetchall()

        
        db.close()
        

        return render_template("users.html", admin=session["admin"], data=x)

    else:
        return redirect("/login")





@dashboard.route("/admins", methods=["POST", "GET"])
def page_dashboard_admins():

    if session.get("admin", None) != None:

        
        if request.method == "POST":


            new_admin = Admin(str(request.form["username"]))

            new_admin.create_admin(str(request.form["password"]), request.form["level"])

            return redirect("/admins")


        else:

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            SELECT
            username, level
            FROM
            admins
            """)

            data = db.cursor.fetchall()


            return render_template("admins.html", admin=session["admin"], data=data)

    else:
        return redirect("/login")



@dashboard.route("/admins/delete")
def page_dashboard_admins_delete():

    if session.get("admin", None) != None:

        if request.args.get("username", None) != None:

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            DELETE
            FROM
            admins
            WHERE
            username = '{request.args["username"]}'
            """)

            db.close()

            return redirect("/admins")

        else:
            return abort(400)

    else:
        return redirect("/login")



