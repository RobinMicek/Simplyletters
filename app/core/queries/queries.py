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


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database


# This class is for making database queries
class Queries():

    def __init__(self):

        self.db = Database()
        self.db.connect()

    
    # Get all newsletters 
    def query_all_newsletters(self):

        self.db.cursor.execute("""
        SELECT
        newsletters_content.title as title,

        newsletters.created_by as created_by,
        newsletters.created as created,
        newsletters.sent as sent,
        newsletters.status as status,
        newsletters.id as id,

        user_groups.name as user_group

        FROM newsletters

        INNER JOIN newsletters_content 
        ON newsletters.id = newsletters_content.id

        INNER JOIN user_groups
        ON newsletters.user_group = user_groups.id 

        ORDER BY newsletters.id DESC
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        return query

    # Get all newsletters w/o the ones made through API
    def query_all_newsletters_without_api(self):

        self.db.cursor.execute("""
        SELECT
        newsletters_content.title as title,

        newsletters.created_by as created_by,
        newsletters.created as created,
        newsletters.sent as sent,
        newsletters.status as status,
        newsletters.id as id,

        user_groups.name as user_group

        FROM newsletters

        INNER JOIN newsletters_content 
        ON newsletters.id = newsletters_content.id

        INNER JOIN user_groups
        ON newsletters.user_group = user_groups.id 

        WHERE user_groups.name != "API"

        ORDER BY newsletters.id DESC
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        return query

    def query_newsletter_info(
        self, 
        id=None
        ):

        self.db.cursor.execute(f""" 
        SELECT
        newsletters_content.title as title,

        newsletters.created_by as created_by,
        newsletters.created as created,
        newsletters.sent as sent,
        newsletters.status as status,
        newsletters.slug as slug,
        newsletters.id as id,

        newsletters_content.perex as perex,
        newsletters_content.perex_header as perex_header,
        newsletters_content.color_main as color_main,
        newsletters_content.color_accent as color_accent,
        newsletters_content.color_text as color_text,

        user_groups.name as user_group,
        user_groups.id as user_group_id

        FROM newsletters

        INNER JOIN newsletters_content 
        ON newsletters.id = newsletters_content.id

        INNER JOIN user_groups
        ON newsletters.user_group = user_groups.id 

        WHERE newsletters.id = "{id}"
        """)
        query_newsletter = self.db.cursor.fetchall()[0]
        
        self.db.cursor.execute(f""" 
        SELECT

        paragraph_id as paragraph_id,
        header as header,
        text as text,
        image as image

        FROM newsletters_paragraphs

        WHERE newsletters_paragraphs.id = "{id}"
        """)
        query_paragraphs = self.db.cursor.fetchall()

        self.db.close()

        query = dict(
            query_newsletter,
            **{"paragraphs": query_paragraphs})

        return query


    def query_user_groups(self):

        self.db.cursor.execute("""
        SELECT
        user_groups.name as name,
        user_groups.id as id,
        user_groups.description as description,

        COUNT(users.firstname) as users

        FROM user_groups    

        LEFT JOIN users_in_groups
        ON user_groups.id = users_in_groups.group_id

        LEFT JOIN users
        ON users_in_groups.user_id = users.id

        GROUP BY
        user_groups.id
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        return query


    def query_newsletter_info_for_render(
        self,
        id = None
        ):

        self.db.cursor.execute(f"""
        SELECT
        newsletters_content.template as template_number,
        newsletters_content.color_main as color_main,
        newsletters_content.color_accent as color_accent,
        newsletters_content.color_text as color_text,

        newsletters_content.title as title,
        newsletters_content.perex as perex,
        newsletters_content.perex_header as perex_header,
        newsletters.slug as slug,
        newsletters.user_group as user_group

        FROM newsletters

        INNER JOIN newsletters_content 
        ON newsletters.id = newsletters_content.id

        INNER JOIN user_groups
        ON newsletters.user_group = user_groups.id 

        WHERE newsletters.id = "{id}"
        """)
        query_newsletter = self.db.cursor.fetchall()[0]


        self.db.cursor.execute(f"""
        SELECT

        header,
        text,
        image

        FROM newsletters_paragraphs

        WHERE id = "{id}"
        """)
        query_paragraphs = self.db.cursor.fetchall()

        self.db.cursor.execute("""
        SELECT 

        footer,
        logo 

        FROM
        newsletters_config
        """)
        query_config = self.db.cursor.fetchall()[0]
        self.db.close()

        query = dict(
            query_newsletter,
            **query_config
            )
        query = dict(
            query,
            **{"paragraphs": query_paragraphs}
        )

        
        return query


    def query_settings(self):

        self.db.cursor.execute("""
        SELECT
    
        logo,
        footer

        FROM 
        newsletters_config
        """)
        
        query = self.db.cursor.fetchall()[0]
        self.db.close()
        
        return query

    
    def query_admins(self):

        self.db.cursor.execute("""
        SELECT
    
        admins.username as username,
        admins.level as level,
        admins.id as id,

        COUNT(newsletters.created_by) as newsletters

        FROM 
        admins

        LEFT JOIN newsletters
        ON admins.username = newsletters.created_by

        GROUP BY admins.username 
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        return query

    
    def query_apps(self):

        self.db.cursor.execute("""
        SELECT

        connected_apps.id as id,
        connected_apps.name as name,
        connected_apps.description as description,
        connected_apps.api_key as api_key,

        user_groups.name as user_group

        FROM connected_apps 

        INNER JOIN user_groups
        ON connected_apps.user_group = user_groups.id 
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        return query

    
    def query_company_info(self):

        self.db.cursor.execute("""
        SELECT

        company_name,
        description

        FROM config

        LIMIT 1
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        return query[0]


    def query_check_fts(self):

        self.db.cursor.execute("""
        SELECT 
            TABLE_NAME
        FROM 
            information_schema.TABLES 
        WHERE
            TABLE_NAME = "config"
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()

        if len(query) == 0:

            return False

        else:

            return True


    # STATS
    def query_number_of_users(self):

        self.db.cursor.execute("""
        SELECT

        COUNT(email) as "users"

        FROM users 
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        try:
            return query[0].get("users", None)
        except:
            return None


    def query_number_of_newsletters(self):

        self.db.cursor.execute("""
        SELECT

        COUNT(id) as "newsletters"

        FROM newsletters
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        try:
            return query[0].get("newsletters", None)
        except:
            return None

    
    def query_last_created_newsletter(self):

        self.db.cursor.execute("""
        SELECT

        created

        FROM newsletters
        
        ORDER BY id DESC

        LIMIT 1
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        try:
            return query[0].get("created", None)
        except:
            return None

    
    def query_most_active_admin(self):

        self.db.cursor.execute("""
        SELECT

        created_by

        FROM newsletters

        ORDER BY COUNT(created_by) DESC
        
        LIMIT 1
        """)
        
        query = self.db.cursor.fetchall()
        self.db.close()
        
        try:
            return query[0].get("created_by", None)
        except:
            return None
        