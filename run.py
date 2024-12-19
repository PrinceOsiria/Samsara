###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
from dae import *

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Auto-Config Setup
if not (discord_bot_token and root_folder_id and years_document_id and private_key_location and bot_workspace_location and local_archive_folder_location):
    print("\n\nProvide Data for Variables in 'run.py' for Faster Setup")
    if not root_folder_id:
        print("\nPlease Provide the id of the root folder in Google Drive:\t")
        root_folder_id = input()
    if not years_document_id:
        print("\nPlease Provide the id of the document to be used for storing 'years'hyperlinks, in Google Drive:\t")
        years_document_id = input()
    if not private_key_location:
        print("\nPlease Provide the path to the private key for your service account:\t")
        private_key_location = input()
    if not bot_workspace_location:
        print("\nPlease Provide the path of the directory this file is in:\t")
        bot_workspace_location = input()
    if not local_archive_folder_location:
        print("\nPlease Provide the path of the archive folder in the same directory as listed above:\t")
        local_archive_folder_location = input()
    if not discord_bot_token:
        print("\nPlease Provide your discord bot token:\t")
        discord_bot_token=input()
        

###########################################################################################################################################
##################################################### Main ################################################################################
###########################################################################################################################################
# Start the bot
dae.run("discord_bot_key")