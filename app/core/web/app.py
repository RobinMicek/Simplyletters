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

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database

from variables import FLASK_SECRET_KEY


# INICIALIZE FLASK
app = Flask(
    __name__,
    static_folder="files",
    )
app.secret_key = FLASK_SECRET_KEY


# IMPORT BLUEPRINTS
from blueprints.b_auth import b_auth
app.register_blueprint(b_auth)



# RUN THE FLASK TEST SERVER
while __name__ == "__main__":
    
    app.run(
        debug=True,
        port=5000,
        host="0.0.0.0"
    )