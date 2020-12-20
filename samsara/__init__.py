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

# Database Model
from samsara.Archive.Models import *

# Google Drive Access Functions
from samsara.Modules.pydrive_wrapper import *

# Bot Options
from samsara.Config import output_options

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Bot Prefix
Samsara = commands.Bot(command_prefix="!")

# Authentication
gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/tyler/Documents/GitHub/Samsara/samsara/Archive/private_key.json", scope)
drive = GoogleDrive(gauth)

# Output Options
output = output_options["all_true"]

###########################################################################################################################################
##################################################### Main ################################################################################
###########################################################################################################################################
# Bot Tasks
from .Tasks import *

# Bot Commands
from .Commands import *

# Bot Events
from .Events import *
