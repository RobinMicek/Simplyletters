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
import mysql.connector
import os
import sys

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


class Database():

    def __init__(self):

        self.name = os.environ.get("SL_DATABASE_NAME", None) 
        self.user = os.environ.get("SL_DATABASE_USER", None) 
        self.password = os.environ.get("SL_DATABASE_PASSWORD", None) 

        self.host = os.environ.get("SL_DATABASE_HOST", None) 
    

    def connect(self):

        self.db = mysql.connector.connect(
            database=self.name, 
            user = self.user, 
            password = self.password, 
            host = self.host, 
            port = "3306"
            )


        self.cursor = self.db.cursor()


    def close(self):

        self.db.commit()

        self.db.close()    


    def initialize(self):
        # Initializes new database with all the necesary tables etc.
        # SQL script is saved in sql/init.sql file. 
        self.connect()

        for x in self.handle_sql_file("init.sql"):

            print("\n----", x, "\n----")

            self.cursor.execute(x)

        self.close()


    def clear(self):
        # Clears used database.
        # SQL script is saved in sql/clear.sql file. 
        self.connect()

        try:
            for x in self.handle_sql_file("clear.sql"):

                print("\n----", x, "\n----")

                self.cursor.execute(x)
        
        except:
            print("Could not clear the DB!")


        self.close()



    def handle_sql_file(self, filemane):
        # This function takes a SQL script file and splits it into
        # individual statements. 
        # I'm doing this because I had problems with executing multiple statements 
        # as one using cursor.exetute(x, multi=True)

        # This function only takes files from the /sql/ directory

        file = f'{open(os.path.join(os.path.dirname(__file__), "sql/" + str(filemane)), "r+").read()}'

        file = file.split(";")

        
        for x in file:
            x.replace(";", "")

        return file
