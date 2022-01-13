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

# Web-Requests Access
import requests

# Database Model
from dae.Archive.Models import *

# Google Drive Access Functions
from dae.Modules.pydrive_wrapper import *

# Media File Compilation
from .Modules.mimecompiler import *

# Bot Options
from dae.Config import output_options, selected_output_option, command_prefix

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Bot Prefix
dae = commands.Bot(command_prefix=command_prefix, help_command=None)

# Output Options
output = output_options[selected_output_option]

###########################################################################################################################################
##################################################### Main ################################################################################
###########################################################################################################################################
# Bot Tasks
from .Tasks import *

# Bot Commands
from .Commands import *

# Bot Events
from .Events import *
