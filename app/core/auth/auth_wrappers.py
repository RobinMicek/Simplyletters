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

# IMPORTS FROM PACKAGES
from flask import session, redirect

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)



# These are wrappers that are used to check if current user 
# has required level to access requested content.

def required_level_one(func):
    def wrap(*args, **kwargs):
        if session.get("account", None) != None and 3 > int(session.get("level", 0)) > 0:

            return func(*args, **kwargs)

        else:
            return redirect("/login")
    
    wrap.__name__ = func.__name__
    return wrap
        

def required_level_two(func):
    def wrap(*args, **kwargs):
        if session.get("account", None) != None and 3 > int(session.get("level", 0)) > 1:

            return func(*args, **kwargs)

        else:
            return redirect("/login")

    wrap.__name__ = func.__name__
    return wrap
        


def required_level_api(func):
    def wrap(*args, **kwargs):
        if session.get("account", None) != None and int(session.get("level", 0) == 3):

            return func(*args, **kwargs)

        else:
            return redirect("/login")

    wrap.__name__ = func.__name__
    return wrap
        