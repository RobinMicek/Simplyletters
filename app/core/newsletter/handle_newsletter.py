"""
******************************************

    This code is part of SimplyLetters

    github.com/RobinMicek/SimplyLetters

------------------------------------------   

    written by Robin Míček

    released under MIT License

******************************************
"""


# Variables in HTML template:
#
#   TITLE - Title of the file
#   LOGO - Company logo
#   PEREX - Short description of the newsletter
#   COLOR-TEXT
#   COLOR-MAIN - Background color
#   COLOR-ACCENT
#   PARAGRAPHS
#   FOOTER
#   NAME
#
# Variables are written using |?|VALUE|?|


# Please note that since I'm using my own style of writing variables,
# the HTML files cannot be used on their own.
# They need to be rendered using this python script!
# I can allow my self to do this, since python is treating those files
# as plain text, completely ignoring the HTML syntax.


# IMPORTS
import os
import sys

import smtplib, ssl
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database

from date import date_now


class Newsletter():
    
    def __init__(self,
        template_number = None,
        color_main = None, color_accent = None, color_text = None, logo = None,
        footer = None, title = None, perex = None, perex_header = None,
        paragraphs = None,
        slug = None, user_group = None
        ):

        self.template_number = template_number
        # Each one of the templates has a number at the end of the name of the file.
        # Because of this we can add basically unlimited number of templates 
        # and let the author decide, which one he wants to use.
        # Each of the templates contains the same variables, so they are interchangeable. 

        self.color_main = color_main
        self.color_accent = color_accent
        self.color_text= color_text

        self.logo = logo

        self.perex_header = perex_header
        self.footer = footer
        self.title = title
        self.perex = perex
        self.paragraphs = paragraphs
        # Paragraphs is a json file with all the paragraphs, 
        # each one includes heading, text and image.
        # Text can include HTML code to add extra functionality.

        self.slug = slug
        self.user_group = user_group


        self.template_file = f'{open(os.path.join(os.path.dirname(__file__), "templates/email_template" + str(self.template_number) + ".html"), "r+").read()}'
        self.template = self.template_file


    def make_slug(self):

        edited_slug = f"{date_now()}-{self.slug}"

        edited_slug = edited_slug.replace(" ", "_")

        return edited_slug


    def add_logos(self):
        
        self.template = self.template.replace("|?|LOGO|?|", self.logo)

    
    def add_title(self):

        self.template = self.template.replace("|?|TITLE|?|", self.title)

    def add_perex(self):

        self.template = self.template.replace("|?|PEREX-HEADER|?|", self.perex_header)

        self.template = self.template.replace("|?|PEREX|?|", self.perex)

    def add_footer(self):

        self.template = self.template.replace("|?|FOOTER|?|", self.footer)

    
    def add_paragraphs(self):

        paragraphs_file =  f'{open(os.path.join(os.path.dirname(__file__), "templates/email_template_paragraph" + str(self.template_number) + ".html"), "r+").read()}'
        paragraphs = paragraphs_file

        all_paragraphs = ""
        
        for x in self.paragraphs:

            print(x)

            paragraph = paragraphs

            paragraph = paragraph.replace("|?|HEADER|?|", x["header"])
            paragraph = paragraph.replace("|?|TEXT|?|", x["text"])

            # Check if paragraph contains image. 
            # If not, replace the |?|IMAGE|?| variable with blank ("").
            if len(x["image"]) != 0:

                image_file = f'{open(os.path.join(os.path.dirname(__file__), "templates/email_template_paragraph_image" + str(self.template_number) + ".html"), "r+").read()}'
                image = image_file.replace("|?|IMAGE|?|", x["image"])  
                
                paragraph = paragraph.replace("|?|IMAGE|?|", image)

            
            else:
                paragraph = paragraph.replace("|?|IMAGE|?|", "")
            
            all_paragraphs = f'{all_paragraphs}{paragraph}'


        self.template = self.template.replace("|?|PARAGRAPHS|?|", all_paragraphs)



    def add_colors(self):

        self.template = self.template.replace("|?|COLOR-MAIN|?|", self.color_main)

        self.template = self.template.replace("|?|COLOR-ACCENT|?|", self.color_accent)

        self.template = self.template.replace("|?|COLOR-TEXT|?|", self.color_text)

    
    def add_date(self):

        self.template = self.template.replace("|?|DATE|?|", date_now())



    def render_email(self):

        # Replace variables
        self.add_logos()
        self.add_title()
        self.add_perex()
        self.add_footer()
        self.add_paragraphs()
        self.add_colors()
        self.add_date()
        

        # Save the file
        file = open(os.path.join(os.path.dirname(__file__), "templates/render.html"), "w+", encoding="utf-8")
        file.write(self.template)

        # Also need to save it into 'static' flask friendly folder for ability to preview it
        # from the flask app
        parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_flask = open(os.path.join(parent_dir, "web/static/renders/render.html"), "w+", encoding="utf-8")
        file_flask.write(self.template)


    def create_newsletter(self, admin = None):

        self.render_email()

        # Add data to database
        database = Database()
        database.connect()
        database.cursor.execute(f"""
        INSERT INTO newsletters
        (
            user_group,
            slug,
            created,
            created_by
        )
        VALUES
        (
            '{self.user_group}',
            '{self.make_slug()}',
            '{date_now()}',
            '{admin}'
        )
        """)
    
        database.cursor.execute(f"""
        INSERT INTO newsletters_content
        (
            id,
            template,
            color_main,
            color_accent,
            color_text,
            title,
            perex,
            perex_header
        )
        VALUES
        (
            LAST_INSERT_ID(),
            '{self.template_number}',
            '{self.color_main}',
            '{self.color_accent}',
            '{self.color_text}',
            '{self.title}',
            '{self.perex}',
            '{self.perex_header}'
        )
        """)

        id = database.cursor.lastrowid

        for x in self.paragraphs:

            header = x["header"]
            text = x["text"]
            image = x["image"]

            database.cursor.execute(f"""
            INSERT INTO newsletters_paragraphs
            (
                id,
                header,
                text,
                image
            )
            VALUES
            (
                '{id}',
                '{header}',
                '{text}',
                '{image}'
            )
            """)


        database.close()

        return id


    def send_email(self,
        id = None,
        group = None, email = None):

        # This function can send emails to both people in group or
        # to a individual email.
        # Set group = True for multiple users in group,
        # Set group = False and email = "email" for individual email

        
        # Render newsletter
        # self.render_email()


        db = Database()
        db.connect()

        # Get email credentials 
        db.cursor.execute("""
        SELECT
        email, password, smtp_server
        FROM
        email_credentials
        """)
        credentials = db.cursor.fetchall()[0]
        
        sender_email = credentials["email"]
        password = credentials["password"]
        smtp_server = credentials["smtp_server"]

        
        def send_email_group():

            db.cursor.execute(f"""
            SELECT
            users.firstname as name, 
            users.email as email,
            users_in_groups.group_id as id

            FROM users
            INNER JOIN users_in_groups
            ON users.id = users_in_groups.user_id 

            WHERE users_in_groups.group_id = '{self.user_group}'
            """)

            users = db.cursor.fetchall()


            for x in users:
                user_name = x["name"]
                receiver_email = x["email"]  

                message = MIMEMultipart("alternative")
                message["Subject"] = str(self.title)
                message["From"] = sender_email
                message["To"] = receiver_email

                # Create the plain-text and HTML version of your message
                #text = "Couldn't load the HTML!"
                html = open(os.path.join(os.path.dirname(__file__), "templates/render.html"), "rb").read().decode('utf-8')

                # Personalize email
                html = html.replace("|?|NAME|?|", str(user_name))

                # Turn these into plain/html MIMEText objects
                #part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")

                # Add HTML/plain-text parts to MIMEMultipart message
                # The email client will try to render the last part first
                #message.attach(part1)
                message.attach(part2)

                # Create secure connection with server and send email
                # context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server) as server:
                    server.login(sender_email, password)
                    server.sendmail(
                        sender_email, receiver_email, message.as_string()
                    )


        
        def send_email_single():
           
            message = MIMEMultipart("alternative")
            message["Subject"] = str(self.title)
            message["From"] = sender_email
            message["To"] = email

            # Create the plain-text and HTML version of your message
            #text = "Couldn't load the HTML!"
            html = open(os.path.join(os.path.dirname(__file__), "templates/render.html"), "rb").read().decode('utf-8')

            # Personalize email
            html = html.replace("|?|NAME|?|", "")

            # Turn these into plain/html MIMEText objects
            #part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            #message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            # context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, email, message.as_string()
                )

    
        if group == True:

            send_email_group()

        elif group == False and email != None:

            send_email_single()
        
        
        # Update record in DB
        db = Database()
        db.connect()
        db.cursor.execute(f"""
        UPDATE newsletters
        SET
        status = 1,
        sent = '{date_now()}'
        WHERE id = '{id}'
        """)

        db.close()
