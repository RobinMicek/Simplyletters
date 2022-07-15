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


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.database_connection import Database



# IMPORTS FLASK
from flask import Flask, session, request, render_template, abort, session


# FLASK INIT
app = Flask(__name__)
app.secret_key = os.environ.get("SL_SECRET-KEY", "simplyletters") 




# FLASK BLUEPRINTS
from fts import fts
app.register_blueprint(fts, url_prefix="/fts")

from login import login
app.register_blueprint(login, url_prefix="/login")

from dashboard import dashboard
app.register_blueprint(dashboard)

from newsletters import dashboard_newsletters
app.register_blueprint(dashboard_newsletters, url_prefix="/newsletters")

from connect import connect
app.register_blueprint(connect, url_prefix="/connected-apps")

from api import api
app.register_blueprint(api, url_prefix="/api")




while __name__ == "__main__":
    app.run(
        debug=True
    )   
