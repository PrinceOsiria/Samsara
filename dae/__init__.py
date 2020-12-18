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
from dae.Archive.Model import Event

# Pymagic MIME Analysis
import magic


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

# Pymagic Instantiation
mime = magic.Magic(mime=True)

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Query drive
def query_drive(query=None):
	if query:
		return drive.ListFile(dict(q = query)).GetList()


# Initialize Drive
def startup_drive():
	return {
		"All Files" : query_drive("trashed = false and mimeType != 'application/vnd.google-apps.folder'"), 					# File List
		"Current Events" : initialize_file_from_drive_file_list(file_list=query_drive(query="title = 'Current Events'")), 	# Folder File
		"Data Entry Form" : initialize_file_from_drive_file_list(file_list=query_drive(query="title = 'Data Entry Form'")),	# File File
		"Evidence" : initialize_file_from_drive_file_list(file_list=query_drive(query="title = 'Evidence'"))				# Folder File
		}


# Initialize file from file list
def initialize_file_from_drive_file_list(file_list=None):

	# Get file title
	def get_title_from_drive_file_list(file_list=None):
		for file in file_list:
			if file["title"]:
				return file["title"]

	# Get file id
	def get_id_from_drive_file_list(file_list=None):
		for file in file_list:
			if file["id"]:
				return file["id"]


	# Initialize File
	if file_list:
		return dict(
			title = get_title_from_drive_file_list(file_list=file_list),
			id = get_id_from_drive_file_list(file_list=file_list)
			)



# Get files in folder via id
def get_child_files_from_drive_id(parent_id=None):
	if parent_id:
		files = []
		for file in query_drive(f"'{parent_id}' in parents and trashed=false"):
			files.append(dict(
					title = file["title"],
					id = file["id"],
					file_mime = file["mimeType"]
				))
		return files


# Download files given a dictionary with title and id pairings for files
def download_drive_files(file_list=None, debug=True):
	for file in file_list:

		# Identify files
		title = file["title"]
		id = file["id"]
		file_mime = file["file_mime"].split("/")


		# Download files
		files = query_drive(f"title = '{title}'")
		for dl in files:
			dl.GetContentFile(title)


			# Search events for an id-evidence match
			os.rename(title, id)
			event = session.query(Event).filter(Event.evidence.contains(id)).first()

			##### DEBUG
			if debug:
				print(f"""
						Event: {event}
					""")


			# Get title and id from event
			if event:
				event_title = event.title
				event_date = event.date
			else:
				print("WARNING: EVENT NOT FOUND - CONTROLLED CRASH INITIATED")


			# Create Event Folders
			event_date = event_date.split("/")

			year = event_date[2]
			month = event_date[0]
			day = event_date[1]

			event_date = f"{year}\\{month}\\{day}"


			# Determine current path
			current_path = os.fspath(pathlib.Path(id).absolute())
			cache_path = os.fspath(pathlib.Path(id).parent.absolute()) + f"\\dae\\Archive\\Cache\\"

			##### DEBUG
			if debug:
				print(f"""
					After downloading and identifying/renaming files
	
						File id: {id} 
						Event title: {event_title}
						Event date: {event_date}
						Current path: {current_path}
						Cache path: {cache_path}
					""")
			

			## Create date directory
			# Year
			date_path = cache_path + f"{year}\\"
			if not os.path.isdir(date_path):
				os.mkdir(date_path)

			# Month
			date_path += f"{month}\\"
			if not os.path.isdir(date_path):
				os.mkdir(date_path)

			# Day
			date_path += f"{day}\\"
			if not os.path.isdir(date_path):
				os.mkdir(date_path)


			##### DEBUG
			if debug:
				print(f"""
					After creating date_path
	
						File id: {id} 
						Event title: {event_title}
						Event date: {event_date}
	
						Current path: {current_path}
						Cache path: {cache_path}
						Date path: {date_path}
				""")



			# Create event directory
			event_path =  date_path + f"{event_title}\\"
			if not os.path.isdir(event_path):
				os.mkdir(event_path)


			##### DEBUG
			if debug:
				print(f"""
					After creating event_path
	
						File id: {id} 
						Event title: {event_title}
						Event date: {event_date}
	
						Current path: {current_path}
						Cache path: {cache_path}
						Date path: {date_path}
						Event path: {event_path}
				""")


			# Create and organize summary file
			summary_path = f"{event_path}\\text"
			if not os.path.isdir(summary_path):
				os.mkdir(summary_path)
			summary = open(f"{summary_path}\\summary.txt", "w+")
			summary.write(event.summary)
			summary.close()


			##### DEBUG
			if debug:
				print(f"""
					After creating event_path
	
						File id: {id} 
						Event title: {event_title}
						Event date: {event_date}
	
						Current path: {current_path}
						Cache path: {cache_path}
						Date path: {date_path}
						Event path: {event_path}
						Summary path: {summary_path}
				""")


			# Create type files
			type_path = event_path + f"{file_mime[0]}\\"
			if not os.path.isdir(type_path):
				os.mkdir(type_path)



			##### DEBUG
			if debug:
				print(f"""
					After creating type_path
	
						File id: {id} 
						Event title: {event_title}
						Event date: {event_date}
	
						Current path: {current_path}
						Cache path: {cache_path}
						Date path: {date_path}
						Event path: {event_path}
						Type path: {type_path}
				""")


			# Organize files by type
			filename = f"{id}.{file_mime[1]}"
			shutil.copy(current_path, type_path + filename)
			os.remove(id)

			
			##### DEBUG
			if debug:
				print(f"""
					After organizing files
	
						File id: {id} 
						Event title: {event_title}
						Event date: {event_date}
	
						Current path: {current_path}
						Cache path: {cache_path}
						Date path: {date_path}
						Event path: {event_path}
						Type path: {type_path}
				""")


###########################################################################################################################################
##################################################### Main ################################################################################
###########################################################################################################################################
# Bot Tasks
from .Tasks import *

# Bot Commands
from .Commands import *

# Bot Events
from .Events import *
