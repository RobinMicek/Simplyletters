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

# This file containts the majority of constant variables. 
# The reason while we store all these variables in one file is.
# so we can have a quick overview see, if a variable that we might need
# is already created - this is especially handy when needing the same 
# variable in multiple files. 
# It also allows us to quickly change things like DB SERVER INFO or API KEYS
# without the need to go through the source code. 


# DATABASE SERVER INFO
DB_HOST = str(os.environ.get("SL_DB_HOST", None))
DB_NAME = str(os.environ.get("SL_DB_NAME", None)) 
DB_USER = str(os.environ.get("SL_DB_USER", None))
DB_PASSWORD = str(os.environ.get("SL_DB_PASSWORD", None))
DB_SSL_CA = str(os.environ.get("SL_DB_SSL_CA", None))


# FLASK
FLASK_SECRET_KEY = str(os.environ.get("SL_FLASK_SECRET_KEY", None))

