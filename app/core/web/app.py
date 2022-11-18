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

from blueprints.b_dashboard import b_dashboard
app.register_blueprint(b_dashboard)

from blueprints.b_newsletters import b_newsletters
app.register_blueprint(b_newsletters)

from blueprints.b_groups import b_groups
app.register_blueprint(b_groups)

from blueprints.b_settings import b_settings
app.register_blueprint(b_settings)

from blueprints.b_admins import b_admins
app.register_blueprint(b_admins)

from blueprints.b_apps import b_apps
app.register_blueprint(b_apps)

from blueprints.b_api import b_api
app.register_blueprint(b_api)

from blueprints.b_fts import b_fts
app.register_blueprint(b_fts)


# RUN THE FLASK TEST SERVER
while __name__ == "__main__":
    
    app.run(
        debug=True,
        port=5001,
        host="0.0.0.0"
    )