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



# Simplyletters uses Dropbox to store email images and other data.


##############################################################
# THIS SCRIPT IS NOT CURRENTLY USED BY SIMPLYLETTER,
# BUT IT MIGHT COME HANDY IN THE FUTURE SO I LEFT IT HERE.
# SIMPLYLETTERS DOES NOT CURRENTLY HAVE CLOUD STORAGE OPTION.
##############################################################


# IMPORTS

import os
import sys

#import dropbox
#from dropbox import DropboxOAuth2FlowNoRedirect

# IMPORTS FROM OTHER FILES
# Fix
sys.path.insert(0, "..")

from database.database_connection import Database



class Handle_Dropbox():

    def __init__(self):

        self.api_token = ""
        


    def upload(self, filename, file, dropbox_folder):

        # target location in Dropbox
        #target = str(dropbox_folder)     # the target folder
        #targetfile = target + filename   # the target path and file name

        # Create a dropbox object using an API v2 key
        #d = dropbox.Dropbox(self.api_token)

        # read the file and upload it

        # upload gives you metadata about the file
        # we want to overwite any previous version of the file
        #meta = d.files_upload(file, targetfile, mode=dropbox.files.WriteMode("overwrite"))

        # create a shared link
        #link = d.sharing_create_shared_link(targetfile)

        # url which can be shared
        #url = link.url

        return "" #url


