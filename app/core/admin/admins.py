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

# IMPORTS
import sys
import os

import hashlib

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.database_connection import Database



# Create 'Admin' class
# This will handle creating users and auth
class Admin():
    def __init__(self, username):
        self.username = username


        db = Database()
        db.connect()
        db.cursor.execute(f"""
        SELECT 
        username, hash
        FROM admins
        WHERE admins.username = '{self.username}'
        """)

        self.query = db.cursor.fetchall()

        db.close()


    # Auth => Check if password is correct to the username
    def auth(self, password):
        if len(self.query) != 0:
            if self.query[0][1] == self.create_hash(password):
                
                return True

            else:
                return False

        else:
            return False


    # Create a new admin
    def create_admin(self, password, level):
        if len(self.query) == 0:
            
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
    def create_hash(self, password):
        return (
            hashlib.sha256(f"{password}{self.username}".encode()).hexdigest()
            )