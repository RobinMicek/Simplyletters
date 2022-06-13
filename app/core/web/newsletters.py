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
# DASHBOARD - NEWSLETTERS

# IMPORTS
import sys
import os



# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.database_connection import Database


# IMPORTS FLASK
from flask import Blueprint, render_template, abort, request, redirect, session

from emailing.create_email import Email_Template



dashboard_newsletters = Blueprint(
    "dashboard_newsletters", 
    __name__,
    template_folder='templates'
)


@dashboard_newsletters.route("/")
def page_newsletters():
    if session.get("admin", None) != None:

        db = Database()
        db.connect()
        db.cursor.execute("""
        SELECT 
        newsletters_content.title,
        user_groups.name,
        newsletters.status,
        newsletters.created,
        newsletters.created_by,
        newsletters.id

        FROM
        newsletters_content 

        INNER JOIN
        newsletters
        ON newsletters_content.id = newsletters.id

        INNER JOIN
        user_groups
        ON newsletters.user_group = user_groups.id 

        ORDER BY newsletters.id DESC
        """)

        newsletters = db.cursor.fetchall() 
        db.close()

        return render_template("newsletters.html", admin=session["admin"], newsletters=newsletters)


    else:
        return redirect("/login")



@dashboard_newsletters.route("/new", methods=["POST", "GET"])
def page_newsletters_new():

    if session.get("admin", None) != None:

        if request.method == "POST":

            db = Database()
            db.connect()
            db.cursor.execute("""
            SELECT
            logo, footer
            FROM
            newsletters_config
            """)

            newsletters_config = db.cursor.fetchall()
            db.close()

            
            new_newsletter = Email_Template(
                request.form["template"],
                request.form["color-main"],
                request.form["color-accent"],
                request.form["color-text"],
                newsletters_config[0][0],
                "",
                newsletters_config[0][1],
                request.form["title"],
                request.form["perex"],
                request.form["perex-header"],
                [],
                request.form["slug"],
                request.form["user-group"]
            )

            new_newsletter.create_newsletter(session["admin"])

            return redirect(f"/newsletters")


        else:

            db = Database()
            db.connect()
            db.cursor.execute("""
            SELECT
            id, name
            FROM
            user_groups
            """)

            user_groups = db.cursor.fetchall()

            db.close()        

            return render_template("newsletters-new.html", admin=session["admin"], user_groups=user_groups)

    else:
        if session.get("admin", None) == None:
            
            return redirect("/login")

        


@dashboard_newsletters.route("/update", methods=["POST", "GET"])
def page_newsletters_update():



    if session.get("admin", None) != None:

        if request.method == "POST":

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            UPDATE
            newsletters_content
            SET
            title = "{request.form["title"]}",
            template = '{request.form["template"]}',
            color_main = '{request.form["color-main"]}',
            color_accent = '{request.form["color-accent"]}',
            color_text = '{request.form["color-text"]}',
            perex_header = "{request.form["perex-header"]}",
            perex = "{request.form["perex"]}"

            WHERE
            id = {request.form["id"]}
            """)

            db.close()

            return redirect(f"/newsletters/update?id={request.form['id']}")


        else:

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            SELECT 
            newsletters_content.title,
            newsletters.slug,
            user_groups.name,
            newsletters_content.template,
            newsletters_content.color_main,
            newsletters_content.color_accent,
            newsletters_content.color_text,
            newsletters_content.perex_header,
            newsletters_content.perex,
            
            newsletters.created,
            newsletters.created_by,

            newsletters.user_group,
            newsletters.id
            
            FROM
            newsletters_content 

            INNER JOIN
            newsletters
            ON newsletters_content.id = newsletters.id

            INNER JOIN
            user_groups
            ON newsletters.user_group = user_groups.id 

            WHERE newsletters.id = '{request.args.get("id", None)}'
            """)

            data = db.cursor.fetchall()[0]

            print(data)

            newsletter_data = {
                "title": data[0],
                "slug": data[1],
                "user-group": data[2],
                "template": data[3],
                "color-main": data[4],
                "color-accent": data[5],
                "color-text": data[6],
                "perex-header": data[7],
                "perex": data[8],
                
                "created": data[9],
                "created-by": data[10],
                
                "user-group-id": data[11],
                "id": data[12]
            }


            db.cursor.execute(f"""
            SELECT
            id, paragraph_id, header, text, image
            FROM
            newsletters_paragraphs
            WHERE
            id = '{request.args["id"]}'
            """)

            data = db.cursor.fetchall()
            paragraph_data = []

            for d in data:

                paragraph_data += [{
                    "id": d[0],
                    "paragraph-id": d[1],
                    "header": d[2],
                    "text": d[3],
                    "image": d[4]
                }]

            print(paragraph_data)

            db.close()        

            return render_template("newsletters-update.html", admin=session["admin"], x=newsletter_data, paragraph_data=paragraph_data)

    else:
        if session.get("admin", None) == None:
            
            return redirect("/login")



@dashboard_newsletters.route("/add-paragraph", methods=["POST"])
def page_newsletters_add_paragraph():

    if session.get("admin", None) != None:


        db = Database()
        db.connect()
        db.cursor.execute(f"""
        INSERT INTO
        newsletters_paragraphs
        (
            id,
            header,
            text,
            image
        )
        VALUES
        (
            {request.form["id"]},
            "{request.form["header"]}",
            "{request.form["text"]}",
            "{request.form["image"]}"
        )
        """)

        db.close()


        return redirect(f"/newsletters/update?id={request.form['id']}#paragraphs")

        


    else:
        if session.get("admin", None) == None:
            
            return abort(405)



@dashboard_newsletters.route("/delete-paragraph")
def page_newsletters_delete_paragraph():

    if session.get("admin", None) != None:

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        DELETE
        FROM
        newsletters_paragraphs
        WHERE
        paragraph_id = {request.args["id"]}
        """)

        db.close()


        return redirect(f"/newsletters/update?id={request.args['n-id']}#paragraphs")

        


    else:
        if session.get("admin", None) == None:
            
            return abort(405)




@dashboard_newsletters.route("/show-render")
def page_newsletters_show_render():

    if session.get("admin", None) != None:

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        select 
        newsletters_content.template,
        newsletters_content.color_main,
        newsletters_content.color_accent,
        newsletters_content.color_text,
        newsletters_content.title,
        newsletters_content.perex,
        newsletters_content.perex_header,
        newsletters.slug,
        newsletters.user_group

        from
        newsletters
        inner join
        newsletters_content
        on newsletters.id = newsletters_content.id 
        
        WHERE newsletters.id = '{request.args["id"]}'
        """)

        n_info = db.cursor.fetchall()[0]

        db.cursor.execute("""
        SELECT
        logo, footer
        FROM
        newsletters_config
        """)

        n_general = db.cursor.fetchall()[0]

        db.cursor.execute(f"""
        SELECT
        header, text, image
        FROM
        newsletters_paragraphs
        WHERE
        newsletters_paragraphs.id = '{request.args["id"]}'
        """)

        x = db.cursor.fetchall()

        n_paragraphs = []

        for p in x:
            n_paragraphs += [{
                "header": p[0],
                "text": p[1],
                "image": p[2]
            }]

        newsletter = Email_Template(
            n_info[0],
            n_info[1],
            n_info[2],
            n_info[3],
            n_general[0],
            "",
            n_general[1],
            n_info[4],
            n_info[5],
            n_info[6],
            n_paragraphs,
            n_info[7],
            n_info[8]

        )

        db.close()

        newsletter.render_email()


        return redirect("/static/renders/render.html")

        


    else:
        if session.get("admin", None) == None:
            
            return abort(405)




@dashboard_newsletters.route("/send-email")
def page_newsletters_send_email():

    if session.get("admin", None) != None:

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        select 
        newsletters_content.template,
        newsletters_content.color_main,
        newsletters_content.color_accent,
        newsletters_content.color_text,
        newsletters_content.title,
        newsletters_content.perex,
        newsletters_content.perex_header,
        newsletters.slug,
        newsletters.user_group

        from
        newsletters
        inner join
        newsletters_content
        on newsletters.id = newsletters_content.id 
        
        WHERE newsletters.id = '{request.args["id"]}'
        """)

        n_info = db.cursor.fetchall()[0]

        db.cursor.execute("""
        SELECT
        logo, footer
        FROM
        newsletters_config
        """)

        n_general = db.cursor.fetchall()[0]

        db.cursor.execute(f"""
        SELECT
        header, text, image
        FROM
        newsletters_paragraphs
        WHERE
        newsletters_paragraphs.id = '{request.args["id"]}'
        """)

        x = db.cursor.fetchall()

        n_paragraphs = []

        for p in x:
            n_paragraphs += [{
                "header": p[0],
                "text": p[1],
                "image": p[2]
            }]

        newsletter = Email_Template(
            n_info[0],
            n_info[1],
            n_info[2],
            n_info[3],
            n_general[0],
            "",
            n_general[1],
            n_info[4],
            n_info[5],
            n_info[6],
            n_paragraphs,
            n_info[7],
            n_info[8]

        )

        db.close()

        if request.args.get("id", None) != None:

            newsletter.send_email(request.args["id"])


        return redirect("/newsletters")

        


    else:
        if session.get("admin", None) == None:
            
            return abort(405)


@dashboard_newsletters.route("/delete-newsletter")
def page_newsletters_delete_newsletter():

    if session.get("admin", None) != None:

        if request.args.get("id", None) != None:

            db = Database()
            db.connect()
            db.cursor.execute(f"""
            DELETE
            FROM
            newsletters
            WHERE
            id = {request.args["id"]}
            """)

            db.cursor.execute(f"""
            DELETE
            FROM
            newsletters_paragraphs
            WHERE
            id = {request.args["id"]}
            """)

            db.cursor.execute(f"""
            DELETE
            FROM
            newsletters_content
            WHERE
            id = {request.args["id"]}
            """)

            db.close()




        return redirect("/newsletters")

        


    else:
        if session.get("admin", None) == None:
            
            return abort(405)

