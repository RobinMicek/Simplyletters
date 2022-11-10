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

import hashlib

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database


# Create 'Admin' class
# This will handle creating users and auth
class Admin():
    def __init__(self, username = None):
        self.username = username


        # Check if account is already in DB
        db = Database()
        db.connect()
        db.cursor.execute(f"""
        SELECT 
        username, hash
        FROM admins
        WHERE username = "{self.username}"
        """)
        self.query = db.cursor.fetchall()
        db.close()

        if len(self.query) == 0:
            self.exists = False
        else:
            self.exists = True


    # Auth => Check if password is correct to the username
    def auth(self, password = None):
        if self.exists == True:
            if self.query[0]["hash"] == self.create_hash(password):
                
                return True

            else:
                return False

        else:
            return False


    def get_level(self):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
        SELECT 
        level
        FROM admins
        WHERE username = "{self.username}"
        """)
        level = db.cursor.fetchall()[0]["level"]
        db.close()

        return level


    # Create a new admin
    def create_admin(self, password = None, level = None):
        if self.exists == False:
            
            db = Database()
            db.connect()
            db.cursor.execute(f"""
            INSERT INTO admins
            (
                username,
                hash,
                level
            )
            VALUES
            (
                '{self.username}',
                '{self.create_hash(password)}',
                '{level}'
            )
            """)

            db.close()


    # This function returns a hash from the password 
    # salted by username
    def create_hash(self, password = None):
        return (
            hashlib.sha256(f"{password}{self.username}".encode()).hexdigest()
            )
