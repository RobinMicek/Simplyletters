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
b_newsletters = Blueprint(
    "newsletters", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_newsletters.route("/newsletters")
@required_level_one
def page_newsletters():
    
    # Check if user wants to see newsletters made through api
    #show_api = str(request.args.get("api", None)).replace("'", "").replace('"', '')
    
    #if show_api == "true":

    newsletters = Queries().query_all_newsletters()

    #else:

    #    newsletters = Queries().query_all_newsletters_without_api()


    return render_template("newsletters.html",
    newsletters = newsletters,
    username = session["account"])


@b_newsletters.route("/newsletter/new", methods=["POST", "GET"])
@required_level_one
def page_newsletter_new():

    if request.method != "POST":

        return render_template("newsletter-new.html",
        user_groups = Queries().query_user_groups(),
        username = session["account"])

    else:

        newsletter = Newsletter(
            template_number = request.form.get("template", None),
            color_main = request.form.get("color-main", None), 
            color_accent = request.form.get("color-accent", None), 
            color_text = request.form.get("color-text", None), 
            title = request.form.get("title", None).replace('"', "'"), 
            perex = request.form.get("perex", None).replace('"', "'"), 
            perex_header = request.form.get("heading", None).replace('"', "'"),
            paragraphs = [],
            slug = request.form.get("slug", None).replace('"', "'"), 
            user_group = request.form.get("user-group", None),
        )
        
        id = newsletter.create_newsletter(admin=session["account"])

        return redirect(f"/newsletter/edit?id={id}")


@b_newsletters.route("/newsletter/edit", methods=["POST", "GET"])
@required_level_one
def page_newsletter_edit():

    if request.method != "POST":

        return render_template("/newsletter-edit.html",
        newsletter = Queries().query_newsletter_info(int(request.args.get("id", None))),
        user_groups = Queries().query_user_groups(),
        username = session["account"])

    else:

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        UPDATE
        newsletters_content
        
        SET
        title = "{request.form["title"].replace('"', "'")}",
        template = '{request.form["template"]}',
        color_main = '{request.form["color-main"]}',
        color_accent = '{request.form["color-accent"]}',
        color_text = '{request.form["color-text"]}',
        perex_header = "{request.form["heading"].replace('"', "'")}",
        perex = "{request.form["perex"].replace('"', "'")}"
        
        WHERE id = {request.form["id"]}
        """)
        db.close()

        return redirect(f"/newsletter/edit?id={request.form['id']}")
        

@b_newsletters.route("/newsletter/add-paragraph", methods=["POST"])
@required_level_one
def page_newsletter_add_paragraph():

    db = Database()
    db.connect()
    db.cursor.execute(f"""
    INSERT INTO newsletters_paragraphs

    (
        id,
        header,
        image,
        text
    )
    VALUES
    (
        "{request.form["id"]}",
        "{request.form["paragraph_title"].replace('"', "'")}",
        "{request.form["paragraph_image"].replace('"', "'")}",
        "{request.form["paragraph_text"].replace('"', "'")}"
    )
    """)
    db.close()

    return redirect(f"/newsletter/edit?id={request.args.get('id', None)}")


@b_newsletters.route("/newsletter/delete-paragraph")
@required_level_one
def page_newsletter_delete_paragraph():

    db = Database()
    db.connect()
    db.cursor.execute(f"""
    DELETE

    FROM
    newsletters_paragraphs

    WHERE 
    paragraph_id = "{request.args.get('paragraph-id', None)}"
    """)
    db.close()

    return redirect(request.referrer)


@b_newsletters.route("/newsletter/render")
@required_level_one
def page_newsletter_render():

    newsletter = Newsletter(**Queries().query_newsletter_info_for_render(request.args.get("id", None)))
    newsletter.render_email()

    return redirect("/files/renders/render.html")



@b_newsletters.route("/newsletter/delete")
@required_level_two
def page_newsletter_delete():

    db = Database()
    db.connect()

    db.cursor.execute(f"""
    DELETE

    FROM
    newsletters

    WHERE 
    id = "{request.args.get('id', None)}"
    """)
    db.cursor.execute(f"""
    DELETE

    FROM
    newsletters_paragraphs

    WHERE 
    id = "{request.args.get('id', None)}"
    """)

    db.cursor.execute(f"""
    DELETE

    FROM
    newsletters_content

    WHERE 
    id = "{request.args.get('id', None)}"
    """)

    db.close()

    return redirect("/newsletters")


@b_newsletters.route("/newsletter/send", methods=["POST"])
@required_level_one
def page_newsletter_send():

    newsletter = Newsletter(**Queries().query_newsletter_info_for_render(request.form.get("id", None)))

    if request.form.get("action", None) == "group":

        newsletter.send_email(
            id = request.form.get("id", None),
            group = True
        )

    elif request.form.get("action", None) == "email":
        
        
        newsletter.send_email(
            id = request.form.get("id", None),
            group = False,
            email = request.form.get("email", None)
        )

    return redirect(f"/newsletter/edit?id={request.form.get('id', None)}")


    