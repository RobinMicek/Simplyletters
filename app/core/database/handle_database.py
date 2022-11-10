"""
******************************************

    This code is part of SimplyLetters

    github.com/RobinMicek/SimplyLetters

------------------------------------------   

    written by Robin Míček

    released under MIT License

******************************************
"""

# PACKAGES IMPORTS
import os
import sys

import mysql.connector

# IMPORTS FROM PACKAGES

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_SSL_CA


class Database():

    def __init__(self):

        self.name = DB_NAME
        self.user = DB_USER 
        self.password = DB_PASSWORD 

        self.host = DB_HOST
        self.ssl_ca = DB_SSL_CA 
    

    def connect(self):

        config = {
            "database": self.name, 
            "user": self.user, 
            "password": self.password, 
            "host": self.host, 
            "port": "3306",
            "buffered": True
        }

        self.db = mysql.connector.connect(**config)


        self.cursor = self.db.cursor(dictionary=True)


    def close(self):

        self.db.commit()

        self.db.close()    


    def initialize(self):
        # Initializes new database with all the necesary tables etc.
        # SQL script is saved in sql/init.sql file. 
        self.connect()

        for x in self.handle_sql_file("init.sql"):

            print("\n----\n", x, "\n----")

            self.cursor.execute(x)

        self.close()

        print("[ALERT] Database has been inicialized!")


    def clear(self):
        # Clears used database.
        # SQL script is saved in sql/clear.sql file. 
        self.connect()

        try:
            for x in self.handle_sql_file("clear.sql"):

                print("\n----\n", x, "\n----")

                self.cursor.execute(x)
        
        except:
            print("[ERROR] Could not clear the DB!")


        self.close()

        print("[ALERT] Database has been cleaned!")


    def handle_sql_file(self, filemane):
        # This function takes a SQL script file and splits it into
        # individual statements. 
        # I'm doing this because I had problems with executing multiple statements 
        # as one using cursor.execute(x, multi=True)

        # This function only takes files from the /sql/ directory

        file = f'{open(os.path.join(os.path.dirname(__file__), "sql/" + str(filemane)), "r+").read()}'

        file = file.split(";")

        
        for x in file:
            x.replace(";", "")

        return file
