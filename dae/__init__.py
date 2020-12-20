###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Local filesystem management imports
import os, pathlib, shutil

# Core Discord Imports
import discord
from discord.ext import commands, tasks

# Project 108 Imports
from .Modules import p108_module as p108

# Google Drive Access
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
import google.auth
import requests

# Database Models
from dae.Archive.Models import *

# Google Drive Functions
from .Modules.pydrive_wrapper import *

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Bot Prefix
dae = commands.Bot(command_prefix="!")

# Authentication
gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/tyler/Documents/GitHub/Samsara/dae/Archive/private_key.json", scope)
drive = GoogleDrive(gauth)

# Select output variables:
output = dict(

    # Automated Cleanup Sequence
    cleanup_sequence = False,

    # Get Current Events
    dirty_current_events = False,
    cleaner_actions = False,
    clean_current_events = False,
    event_internalization = False,

    # Update Database
    database_update = False
  )

###########################################################################################################################################
##################################################### Main ################################################################################
###########################################################################################################################################
# Bot Tasks
from .Tasks import *

# Bot Commands
from .Commands import *

# Bot Events
from .Events import *
