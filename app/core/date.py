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

import datetime

def date_now():

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    
    return str(date)