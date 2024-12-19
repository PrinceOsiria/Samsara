###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Local filesystem management imports
import os, pathlib, shutil

# Core Discord Imports
import discord
from discord.ext import commands, tasks
import time

# Web-Requests Access
import requests

# SQL-Alchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

# Google Drive Access
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from googleapiclient.discovery import build
import google.auth

# Google Text-To-Speech
import gtts
from playsound import playsound
from mutagen.mp3 import MP3
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import *

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Drive Filesystem Configuration
root_folder_id = "" # ID of root drive folder in Google Drive Archive
years_document_id = ""# ID of document to store years Hyperlinks

# Local Filesystem Configuration
private_key_location = "" # Google Service Account Private Key Location (Store in Archive)
bot_workspace_location = "" # Make this the same directory as 'run.py'
local_archive_folder_location="" # The Archive folder in the same directory as 'run.py'

# Discord Bot Configuration
discord_bot_token = "" 
command_prefix = "!" 

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
        

## Debugging Options
## MANUAL
# Prevent the bot from looping on an error
debug_halt = None
# Skip portions of code
debug_skip = None

## AUTOMATIC
# Rebuild the cloud if the local filesystem is missing (results in errors if cloud is occupied)
smart_debug_skip = False
# Turns debug options off
production_mode = True


# Reconfigure Configs
if production_mode:
	debug_halt = False
	debug_skip = False
	smart_debug_skip=False

if smart_debug_skip:
	if "archive.db" not in os.listdir(bot_workspace_location[:-4]): 
		debug_skip = False
		debug_halt = True
	else:
		debug_skip = True
		debug_halt = False


# Output options
selected_output_option = "custom"


# Output Configurations
output_options = dict(

	custom = dict(
			cleanup_sequence = True,
			dirty_current_events = False,
			cleaner_actions = False,
			clean_current_events = False,
			event_internalization = True,
			database_update = True,
			new_events = True,
			new_events_plus = True,
			new_events_more = False,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = True,
			identify_new_videos_more = False,
			generate_new_videos = True,
			generate_new_videos_more = False
	),

	minimal_med = dict(
			cleanup_sequence = True,
			dirty_current_events = False,
			cleaner_actions = True,
			clean_current_events = False,
			event_internalization = False,
			database_update = True,
			new_events = True,
			new_events_plus = False,
			new_events_more = False,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = False,
			identify_new_videos_more = False,
			generate_new_videos = True,
			generate_new_videos_more = False
	),

	minimal_max = dict(
			cleanup_sequence = True,
			dirty_current_events = False,
			cleaner_actions = True,
			clean_current_events = False,
			event_internalization = False,
			database_update = True,
			new_events = True,
			new_events_plus = True,
			new_events_more = False,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = True,
			identify_new_videos_more = False,
			generate_new_videos = True,
			generate_new_videos_more = True
	),

	all_false = dict(
			cleanup_sequence = False,
			dirty_current_events = False,
			cleaner_actions = False,
			clean_current_events = False,
			event_internalization = False,
			database_update = False,
			new_events = False,
			new_events_plus = False,
			new_events_more = True,
			drive_scan = False,
			cloud_integrity_check = False,
			identify_new_videos = False,
			identify_new_videos_more = False,
			generate_new_videos = False,
			generate_new_videos_more = False
	),

	all_true = dict(
			cleanup_sequence = True,
			dirty_current_events = True,
			cleaner_actions = True,
			clean_current_events = True,
			event_internalization = True,
			database_update = True,
			new_events = True,
			new_events_plus = True,
			new_events_more = True,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = True,
			identify_new_videos_more = True,
			generate_new_videos = True,
			generate_new_videos_more = True
	)
)

# Authentication
gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(private_key_location, scope)
service = build('docs', 'v1', credentials=gauth.credentials)
drive = GoogleDrive(gauth)
docs = service.documents()

# Bot Prefix
dae = commands.Bot(command_prefix=command_prefix, help_command=None)

# Output Options
output = output_options[selected_output_option]

# SQLite database creation and initialization
engine = create_engine('sqlite:///dae/Archive/archive.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


###########################################################################################################################################
##################################################### Main ################################################################################
###########################################################################################################################################
# Bot Initialization
@dae.event
async def on_ready():
	
	if "archive.db" not in os.listdir(bot_workspace_location[:-4]):
		print("Existing Archive Not Found, Creating One Now...")
		refresh_database()
	
	if not samsara.is_running():
			samsara.start()

# Bot Loop
@tasks.loop(hours=12)
async def samsara():

	# Non-Optional Output
	if output: print(f"""
###########################################################################################################################################
Codename Samsara is: ONLINE
""")


	# Debug Halt
	if debug_halt: print("Please Press Enter to Begin"); input()

	# Automated Cleanup - N.I.T.E.
	initiate_automated_cleanup()

	# Debug Skip - unindent the part you wish to resume from
	if not debug_skip:
		# Initialization and Validation - N.I.T.E.
		if not production_mode:
			scan_drive()
			validate_cloud_integrity()

		# D.A.E.
		update_database(get_current_events())
		
		# N.I.T.E.
		new_events = identify_new_events()
		if new_events:
			archive_events(new_events)
			generate_timeline_videos(identify_new_videos())
			initiate_automated_cleanup()

	# Non-Optional Output
	if output: print(f"""
Codename Samsara is: OFFLINE
###########################################################################################################################################""")

# This stupid shit must be run first - otherwise certain (if not all) api features will not work
query_drive(f"'{drive_root_folder_id}' in parents")

# Start the bot
dae.run(discord_bot_token)


###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################


############################################################
#Custom Alphabet Generator
#*Returns alphabet as a list
def create_alphabet(AlphabetKey):
    #initializes variables for alphabet key cleaner
    i = 0
    StrippedAlphabetKey = ""
    Alphabet = list("abcdefghijklmnopqrstuvwxyz")
    AlphabetKey = clean_text(AlphabetKey.lower(), Alphabet)

    #cleans alphabet key
    while i < len(AlphabetKey):
      if AlphabetKey[i] not in StrippedAlphabetKey:
          StrippedAlphabetKey = StrippedAlphabetKey + AlphabetKey[i]
      i = i + 1
      
    #initializes variables for alphabet generator
    AlphabetKey = list(StrippedAlphabetKey)

    #Cleans standard alphabet
    i = 0
    while i < len(AlphabetKey):
      x = (ord(AlphabetKey[i]) - 97)
      Alphabet[x] = " "
      i = i + 1

    #creates alphabet and cleans for export
    Alphabet = "".join(Alphabet)
    AlphabetKey = "".join(AlphabetKey)
    Alphabet = AlphabetKey + Alphabet
    Alphabet = Alphabet.replace(" ", "")
    Alphabet = list(Alphabet)

    #Returns alphabet as a list
    return (Alphabet)
############################################################



############################################################
#Text standardization
#*Returns cleaned text in lowercase string by checking to see if each char exists in a given alphabet
def clean_text(DirtyText, Alphabet):
    #initializes text cleaner
    CleanText = ""
    DirtyText = list(DirtyText)

    #cleans text
    x = 0
    while x < len(DirtyText):
      if DirtyText[x] in Alphabet:
          CleanText = CleanText + DirtyText[x]
      elif DirtyText[x] == "~":#Used to clean keys without losing layers
          CleanText = CleanText + DirtyText[x]
      x = x + 1

    #returns cleaned text in lowercase string
    return CleanText
############################################################



############################################################
#Hels Labyrinth Brute Force Attacker
#*Exports results.txt + outputs verbose results
def brute_hels(Alphabet, Keys, CipherText):
    #Imports a thing
    from itertools import permutations
      
    #Initializes Variables
    Keys = Keys.split()
    Combos = []
    file = open("testfile.txt","w") 

    #Shuffles through combinations of keys
    x = 1
    while x <= len(Keys):
      for i in permutations(Keys, x): 
          tmp = " ".join(list(i))
          foo = decode_hels(Alphabet, tmp, CipherText)
          print("\n" + "keys:" + str(tmp) + "|" + "result:" + str(foo))
          file.write("\n" + "keys:" + str(tmp) + "|" + "result:" + str(foo))    
      x = x + 1
    file.close()
############################################################



############################################################
#Hels Labyrinth Decoder
#*Returns lowercase cleartext
def decode_hels(Alphabet, Keys, CipherText):
    #Cycles through each key
    x = 0
    while x < len(Keys):

      #Initializes Variables
      CipherText = list(CipherText)#splits ciphertext into letters
      Keys[x] = list(Keys[x])#splits key into letters
      NumberKey = []
      NumberText = []
      
      #Assigns each letter in the key a number (Based on alphabet given)
      i = 0
      while i < len(Keys[x]):
          tmp = Keys[x][i]
          foo = Alphabet.index(tmp)
          NumberKey.append(foo)
          i = i + 1

      #Assigns each letter in the ciphertext a number (Based on alphabet given)
      i = 0
      while i < len(CipherText):
          tmp = CipherText[i]
          foo = Alphabet.index(tmp)
          NumberText.append(foo)
          i = i + 1

      #Initializes Variables
      Message = []

      #If the key is longer than the ciphertext...
      if len(NumberKey) >= len(NumberText):

          #Generates "Masterkey"
          i = 0
          while i < len(NumberText):
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = tmp - foo

            NumberKey.append(bar)

            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(NumberKey):
            if NumberKey[i] < 0:
                NumberKey[i] = NumberKey[i] + 26
            else:
                i = i + 1

          #Uses "Masterkey"
          i = 0
          while i < len(NumberText):
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = tmp - foo
            Message.append(bar)
            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(Message):
            if Message[i] < 0:
                Message[i] = Message[i] + 26
            else:
                i = i + 1

          #Converts numbers to letters
          i = 0
          while i < len(Message):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1
          Message = "".join(Message)

      #If the key is shorter than the ciphertext...
      elif len(NumberKey) < len(NumberText):
          #Initializes Variable
          Difference = (len(NumberText) - len(NumberKey))

          #Generates "Masterkey"
          i = 0
          while i < Difference:
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = tmp - foo
            NumberKey.append(bar)

            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(NumberKey):
            if NumberKey[i] < 0:
                NumberKey[i] = (NumberKey[i] + 26)
                i = i + 1
            elif NumberKey[i] > 25:
                NumberKey[i] = NumberKey[i] - 26
            else:
                i = i + 1

          #Uses Masterkey
          i = 0
          while i < len(NumberKey):
            tmp = NumberKey[i]
            foo = NumberText[i]
            bar = foo - tmp

            Message.append(bar)

            i = i + 1

          #Lines up numbers with alphabet
          i = 0
          while i < len(Message):
            if Message[i] < 0:
                Message[i] = (Message[i] + 26)
                i = i + 1
            elif Message[i] > 25:
                Message[i] = Message[i] - 26
            else:
                i = i + 1

          #Converts numbers to letters
          i = 0
          while i < len(NumberKey):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1

          #Converts message from a list of letters to a string
          Message = "".join(Message)

      #Initializes Variables
      NumberText = []
      CipherText = Message

      x = x + 1
      #Loops through next key if applicable

    #Returns cleartext as a lowercase string
    return CipherText
############################################################



############################################################
#Hels Labyrinth Encoder
#*Returns lowercase ciphertext
# input = 
# alphabet as list
# keys as list
# Cleantext as lowercase string
def encode_hels(Alphabet, Keys, CipherText):
    #Loops through keys
    x = 0
    while x < len(Keys):
      #Initializes Variables
      CipherText = list(CipherText)
      Keys[x] = list(Keys[x])
      NumberKey = []
      NumberText = []

      #Assigns each letter in each key to numbers based on given alphabet
      i = 0
      while i < len(Keys[x]):
          tmp = Keys[x][i]
          foo = Alphabet.index(tmp)
          NumberKey.append(foo)
          i = i + 1

      #Assigns each letter in the cleartext to numbers based on given alphabet
      i = 0
      while i < len(CipherText):
          tmp = CipherText[i]
          foo = Alphabet.index(tmp)
          NumberText.append(foo)
          i = i + 1

      #Initializes Variables
      Message = []

      if len(NumberKey) >= len(NumberText):

          i = 0
          while i < len(NumberText):
            tmp = NumberText[i]
            foo = NumberKey[i]

            Message.append(tmp + foo)

            i = i + 1
          i = 0
          while i < len(Message):
            if Message[i] > 25:
                Message[i] = Message[i] - 26
                i = i + 1
            else:
                i = i + 1

          i = 0
          while i < len(Message):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1
          Message = "".join(Message)

      elif len(NumberKey) < len(NumberText):
          Difference = (len(NumberText) - len(NumberKey))

          i = 0
          while i < Difference:
            tmp = NumberText[i]
            NumberKey.append(tmp)

            i = i + 1

          i = 0
          while i < len(NumberKey):
            tmp = NumberText[i]
            foo = NumberKey[i]
            bar = foo + tmp
            Message.append(bar)
            i = i + 1

          i = 0
          while i < len(NumberKey):
            if Message[i] > 25:
                Message[i] = (Message[i] - 26)
                i = i + 1
            else:
                i = i + 1

          i = 0
          while i < len(NumberKey):
            tmp = Alphabet[Message[i]]
            Message[i] = tmp
            i = i + 1

          Message = "".join(Message)

      NumberText = []
      CipherText = Message

      x = x + 1
      
    return CipherText
############################################################



############################################################
#ROT13
#*returns lowercase cleartext
def rot13(CipherText):
    #Imports a thing 
    import codecs

    #Initializes Decoding Variables
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    CipherText = clean_text(CipherText, alphabet)

    #Run decoding program
    return(codecs.decode(CipherText, 'rot_13'))
############################################################



############################################################
#XIO Decoder
#*Returns lowercase cleartext
def decode_xio(message):
    #Initializes variables
    MORSE_CODE_DICT = { 'A':'XI', 'B':'IXXX', 'C':'IXIX', 'D':'IXX', 'E':'X', 'F':'XXIX', 'G':'IIX', 'H':'XXXX', 'I':'XX', 'J':'XIII', 'K':'IXI', 'L':'XIXX', 'M':'II', 'N':'IX', 'O':'III', 'P':'XIIX', 'Q':'IIXI', 'R':'XIX', 'S':'XXX', 'T':'I', 'U':'XXI', 'V':'XXXI', 'W':'XII', 'X':'IXXI', 'Y':'IXII', 'Z':'IIXX', '1':'XIIII', '2':'XXIII', '3':'XXXII', '4':'XXXXI', '5':'XXXXX', '6':'IXXXX', '7':'IIXXX', '8':'IIIXX', '9':'IIIIX', '0':'IIIII', ', ':'IIXXII', '?':'XXIIXX', '/':'IXXIX', '-':'IXXXXI', '!':'IXIXII'}
    decipher = '' 
    citext = ''

    #decodes XIO 
    for letter in message: 
      if letter != 'O': 
          citext += letter
      elif letter == 'O':
            if citext in MORSE_CODE_DICT.values():
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = '' 
      elif letter != ' ':
          citext += letter
      elif letter == ' ':
          if citext in MORSE_CODE_DICT.values():
            decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
            decipher += ' '
            citext = ''
      else:
            print(citext, " = ??? ")
            decipher +=" ??? "
            citext = ''
      
    #Returns lowercase cleartext
    return decipher
############################################################



############################################################
#XIO Encoder
#*Returns lowercase ciphertext
def encode_xio(message):
    #Initializes variables
    MORSE_CODE_DICT = { 'XI':'A', 'IXXX':'B', 'IXIX':'C', 'IXX':'D', 'X':'E', 'XXIX':'F', 'IIX':'G', 'XXXX':'H', 'XX':'I', 'XIII':'J', 'IXI':'K', 'XIXX':'L', 'II':'M', 'IX':'N', 'III':'O', 'XIIX':'P', 'IIXI':'Q', 'XIX':'R', 'XXX':'S', 'I':'T', 'XXI':'U', 'XXXI':'V', 'XII':'W', 'IXXI':'X', 'IXII':'Y', 'IIXX':'Z', 'XIIII':'1', 'XXIII':'2', 'XXXII':'3', 'XXXXI':'4', 'XXXXX':'5', 'IXXXX':'6', 'IIXXX':'7', 'IIIXX':'8', 'IIIIX':'9', 'IIIII':'0', 'IIXXII':', ', 'XXIIXX':'?', 'IXXIX':'/', 'IXXXXI':'-', 'IXIXII':'!'}
    decipher = '' 

    #encodes XIO 
    for letter in message: 
      if letter != ' ':
            if letter in MORSE_CODE_DICT.values():
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(letter)]
                decipher += "O"
            #Replaces unknown chars with " ??? "
            else:
                print(letter, ' = ??? ')
                decipher += ' ??? '
            
      #Allows for spaces
      elif letter == ' ':
          decipher += ' '
      
    #Returns lowercase cleartext
    return decipher
############################################################


# Refresh database - WARNING THIS COMMAND DELETES EVERYTHING
def refresh_database():
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

# Add to database
def add_to_db(some_object):
	session.add(some_object)
	session.commit()

# Download Drive Files from Directory
def download_drive_dir_files(id=None):

	# Fetch Directory Contents
  file_list = list_drive_directory(id=id)

  # Internalize Directory Contents
  titles = file_list['titles']
  mimeTypes = file_list['mimeTypes']
  ids = file_list['ids']


	# Download Files
  i= 0
  for id in ids:
    # Establish Filename
    file_name = id + "." + mimeTypes[i].split('/')[1]

    # Fetch Desired File
    export = drive.CreateFile({'id':id})
    print(f"\nDownloading {titles[i]} From Drive...\n")
    
    # Download the file and move on to the next one if there are any
    export.GetContentFile(bot_workspace_location + file_name)
    i+=1


# Download Drive File
def download_drive_file(id=None, file_name=None, directory=None):
  # Get the file
  file = get_drive_file(id=id)
  
  # Non-Optional Output
  print(f"\nDownloading {file['title']} with id {id} from drive to {directory} with file name {file_name}")

  # Download the file
  file.GetContentFile(directory + file_name)

# List Drive Directory
def list_drive_directory(id=None):
  return query_drive(f"'{id}' in parents")


# Create Drive Folder
def create_drive_folder(id=None, title=None):
  file1 = drive.CreateFile({
    'title': title, 
    'parents': [{'id':id}],
    'mimeType': 'application/vnd.google-apps.folder'
    })
  file1.Upload()
  return file1["id"]


# Trash Drive Folder
def trash_drive_folder(id=None):
  file1 = drive.CreateFile({'id':id})
  file1.Trash()


# Delete Drive Folder
def delete_drive_folder(id=None):
  file1 = drive.CreateFile({'id':id})
  file1.Delete()

# Copy Drive File
def copy_drive_file(file_id=None, copy_title=None):
  copied_file = {'title': copy_title}
  file_data = drive.auth.service.files().copy(fileId=file_id, body=copied_file).execute()

  return file_data['id']

# Copy Drive File to Folder
def copy_drive_file_to_folder(file_id=None, copy_title=None, parent_id=None):
  copy_id = copy_drive_file(file_id=file_id,copy_title=copy_title)
  move_drive_file(file_id=copy_id, parent_id=parent_id)
  return copy_id


# Move Drive File
def move_drive_file(file_id=None, parent_id=None):
  files = drive.auth.service.files()
  file  = files.get(fileId= file_id, fields= 'parents').execute()
  prev_parents = ','.join(p['id'] for p in file.get('parents'))
  file  = files.update( fileId = file_id,
                        addParents = parent_id,
                        removeParents = prev_parents,
                        fields = 'id, parents',
                        ).execute()
  return file["id"]

# Get Drive File
def get_drive_file(id=None):
  file = drive.CreateFile()
  file['id'] = id
  file.Upload()
  return file


# Check listing of files for a matching title
def check_files_for_title(files=None,title=None):
  if title in files["titles"]:
    index = files["titles"].index(title)

    return dict(
      title = files["titles"][index],
      id = files["ids"][index],
      mimeType = files["mimeTypes"][index]
    )


# Check listing of files for a matching id
def check_files_for_id(files=None,id=None):
  if id in files["ids"]:
    index = files["ids"].index(id)

    return dict(
      title = files["titles"][index],
      id = files["ids"][index],
      mimeType = files["mimeTypes"][index]
    )


# Get file title
def get_titles_from_fileList(fileList):
  titles = []
  for file in fileList:
    if file["title"]:
      titles.append(file["title"])
  return titles

  
# Get file id
def get_ids_from_fileList(fileList):
  titles = []
  for file in fileList:
    if file["id"]:
      titles.append(file["id"])
  return titles

  # Get file mime
def get_mimes_from_fileList(fileList):
  titles = []
  for file in fileList:
    if file["mimeType"]:
      titles.append(file["mimeType"])
  return titles

# Query drive & Internalize the results
def query_drive(query):
  fileList = drive.ListFile(dict(q = query)).GetList()
 
  return dict(
    titles = get_titles_from_fileList(fileList),
    ids = get_ids_from_fileList(fileList),
    mimeTypes = get_mimes_from_fileList(fileList)
    )

# Create Document
def create_drive_document(title=None, parent_id=None):
  file1 = drive.CreateFile({
      'title': title, 
      'parents': [{'id':parent_id}],
      'mimeType': 'application/vnd.google-apps.document'
  })
  file1.Upload()
  return file1["id"]
  

# Rename Document
def rename_drive_document(id=None,title=None):
  files = drive.auth.service.files()
  file1 = files.get(fileId=id).execute()
  file1['title'] = title
  files.update(
    fileId=id,
    body=file1,
    newRevision=True
    ).execute()


# Insert Text to Document
def insert_text_to_drive_document(id=None, text=None, index=1, link=None, font="Anonymous Pro", font_size=30):
  offset = len(text)

  if link:
      content = [
        {'insertText': {
          'location': {'index': index},
          'text':text + "\n"}
        },
        {
          'updateTextStyle': {
            'range': {
                'startIndex': index,
                'endIndex': index + offset
            },
            'textStyle': {
              'link': {'url': link},
              'weightedFontFamily': {
                'fontFamily': font},
                'fontSize': {
                  'magnitude': font_size,
                  'unit': 'PT'
                },
            },
            'fields': 'link,weightedFontFamily,fontSize'
          }
        }]
  else:
      content = [
        {'insertText': {
          'location': {'index': index},
          'text':text + "\n"}
        },
        {
          'updateTextStyle': {
            'range': {
                'startIndex': index,
                'endIndex': index + offset
            },
            'textStyle': {
              'weightedFontFamily': {
                'fontFamily': font},
                'fontSize': {
                  'magnitude': font_size,
                  'unit': 'PT'
                },
            },
            'fields': 'weightedFontFamily,fontSize'
          }
        }]

  docs.batchUpdate(documentId=id,body={'requests': content}).execute()


# Upload Files
def upload_file_to_drive(file=None, directory=None, parent_id=None, file_name=None):
  file1 = drive.CreateFile({'title': file_name})
  file1.SetContentFile(directory+file)
  print("\nUploading file to drive...")
  file1.Upload()
  return move_drive_file(file_id=file1['id'], parent_id=parent_id)



# Create Document from Template
def create_document_from_template(template_id=None, batch_update=None, target_directory=None, file_title=None):
  file = copy_drive_file_to_folder(file_id=template_id, parent_id=target_directory, copy_title=file_title)
  docs.batchUpdate(documentId=file, body={'requests': batch_update}).execute()
  return file

# Convert Text to Audio File
def convert_text_to_audio_file(text=None, directory=None, file_name=None):
	gtts.gTTS(text).save(directory+file_name+".mp3")
	return (file_name+".mp3")

# Determine Length of audio file
def determine_length_of_audio_file(verbose=True, file=None):
	if verbose: print(file)
	return MP3(file).info.length


# Generate Gif File
def generate_gif_file(directory=None, directory_modifier="", files=None, file_name=None, length=None, image_size=(500,500), length_delay=500, verbose=True):

	# Initialize the output filename
	output_file_name = directory + directory_modifier + file_name + ".gif"
	if verbose: print(f"Output file name: {output_file_name}\nOutput file Directory: {directory}")

	# Optional Output
	if verbose: print(f"Seeking these files: {files}")

	# Scan directory for requested files
	found_files = []
	for file in os.listdir(directory):
		if file in files:
			found_files.append(Image.open(directory+file).resize(size=image_size))
	img = found_files[0]
	if verbose: print(f"Found Files:{found_files}")

	# Modify length input (expected movipy audio length) to work with PIL
	adjusted_length = ((length*1000) + length_delay)/len(files) 
	if verbose: print(f"Length of gif adjusted, saving file")

	# Output the file
	img.save(fp=output_file_name, format='GIF', save_all=True, duration=adjusted_length, loop=0, append_images=found_files)
	if verbose: print(f"File Saved as {file_name}.gif")

	# Return the filename
	return file_name + ".gif"


# Compile Audio Files
def compile_audio_files(files=None, directory=None, file_name=None, file_format="mp3"):
	
	supported_filetypes = ["mp4", "mp3", "flv", "ogg", "wma", "aac", "wav", "mpeg", ]
	supported_files = []

	# Filter and collect the desired files - NOTE: If forms are configured correctly this becomes redundant
	for file in os.listdir(directory):
		if file in files:
			filetype = file.split(".")[1]

			if filetype == "x-wav":
				filetype = "wav"

			if filetype in supported_filetypes:
				supported_files.append(AudioSegment.from_file(directory+file, filetype))

	# Combine the supported audio segments
	output = AudioSegment.empty()
	for file in supported_files:
			output += file

	# Export the recombined audio file
	output.export(directory+file_name, format=file_format)
	return file_name


# Compile Video Files
def compile_video_files(files=None, directory=None, file_name=None, file_size=(500,500)):
	supported_filetypes = ["avi", "mp4"]
	supported_files = []

	# Filter and collect the desired files - NOTE: If forms are configured correctly this becomes redundant
	for file in os.listdir(directory):
		if file in files:
			filetype = file.split(".")[1]

			if filetype in supported_filetypes:
				clip = VideoFileClip(directory+file)
				supported_files.append(clip.resize(file_size))
			else: print(filetype)


	# Combine the video clips
	output = concatenate_videoclips(supported_files, method="compose")

	# Export the recombined video file
	output.write_videofile(directory+file_name)
	return file_name


# Create Video
def create_video(directory=None, audio=None, video=None, gif=None, gif_audio=None, file_name=None, verbose=True, blank_video_directory=None, blank_video=None, blank_png_directory=None, blank_png=None, file_size=(500, 500)):

	# Optional Output
	if verbose: print(f"Internalizing gif:\t{directory+gif}")

	# Internalize gif
	gif = VideoFileClip(directory + gif)
	gif.resize( file_size)

	# Optional Output
	if verbose: print(f"Adding Audio to Gif:\t{directory+gif_audio}")

	# Play audio over gif
	gif.audio = AudioFileClip(directory + gif_audio)

	# Optional Output
	if verbose: print(f"Internalizing Video:\t{directory+video}")

	# Video File
	if os.path.exists(directory+video):
		video = VideoFileClip(directory + video)
		video.resize( file_size)

	else:
		if verbose: print(f"{directory+video} was not Found")

		# Interferance Patch
		video = VideoFileClip(blank_video_directory + blank_video).subclip(10, 11)

	# Audio File
	if os.path.exists(directory+audio):
		tmp_audio = VideoFileClip(directory + generate_gif_file(directory=blank_png_directory, directory_modifier="tmp/", files=[blank_png], file_name=f"{file_name} - Audio Compilation Gif", length=determine_length_of_audio_file(file=directory+audio), image_size=(1000,1000), length_delay=0))
		tmp_audio.audio = AudioFileClip(directory + audio)
		audio = tmp_audio
	else:
		if verbose: print(f"{directory+audio} was not Found")

		# Interferance Patch
		audio = VideoFileClip(blank_video_directory + blank_video).subclip(10, 11)



	# Combine the Clips
	output = concatenate_videoclips([gif, video, audio])

	# Optional Output
	if verbose: print(f"Writing Video File:\t{directory+file_name}")

	# Export the video file
	output.write_videofile(directory+file_name)

# Scan drive
def scan_drive(root_folder_id = root_folder_id):

	if output: print(f"""\n#####################################################\nSCANNING DRIVE\n""")


	# Scan Root Folder
	root_files = query_drive(f"'{root_folder_id}' in parents")


	# Check to see if the Root Archive has been initialized yet
	if not session.query(Drive).filter_by(root_folder_id=root_folder_id).first():
		
		# Optional Output
		if output["drive_scan"]: print("Copying Drive IDs into Internal Records")




		# Optional Output
		if output["drive_scan"]: print("\nLooking for 'N.I.T.E.':")
		
		# Scan Root Files for a matching title
		NITE_folder_id = check_files_for_title(files=root_files, title="N.I.T.E.")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was Found with ID: {NITE_folder_id}\n")
		



		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'D.A.E.':")
		
		# Scan Root Files for a matching title
		DAE_folder_id = check_files_for_title(files=root_files, title="D.A.E.")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was Found with ID: {DAE_folder_id}\n")

		



		# Scan DAE Folder
		DAE_files = query_drive(f"'{DAE_folder_id}' in parents")

		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Archive':")
		
		# Scan Root Files for a matching title
		archive_folder_id = check_files_for_title(files=DAE_files, title="Archive")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was Found with ID: {archive_folder_id}\n")




		# Scan NITE Folder
		NITE_files = query_drive(f"'{NITE_folder_id}' in parents")

		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Evidence':")
		
		# Scan for Data Collection Folder
		data_collection_folder_id = check_files_for_title(files=NITE_files, title="Data Collection")["id"]
		data_collection_files = query_drive(f"'{data_collection_folder_id}' in parents")

		# Scan for Evidence Folder
		evidence_folder_id = check_files_for_title(files=data_collection_files, title="Evidence")["id"]

		# Optional Output
		if output["drive_scan"]: print(f"\tFile was Found with ID: {evidence_folder_id}\n")



		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Current Events':")
		
		# Scan Root Files for a matching title
		current_events_file_id = check_files_for_title(files=NITE_files, title="Current Events")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was Found with ID: {current_events_file_id}\n")


		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Templates':")
		
		# Scan Root Files for a matching title
		template_folder_id = check_files_for_title(files=DAE_files, title="Templates")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was Found with ID: {template_folder_id}\n")




		# Iternalize the IDs of the required drive folders
		drive_map = Drive(template_folder_id=template_folder_id, root_folder_id=root_folder_id, NITE_folder_id=NITE_folder_id, DAE_folder_id=DAE_folder_id, archive_folder_id=archive_folder_id, evidence_folder_id=evidence_folder_id, current_events_file_id=current_events_file_id)
		add_to_db(drive_map)

		# Optional Output
		if output["drive_scan"]: print(f"\nA Drive Map was Created:\n\t{drive_map}\n")

	else:
		if output["drive_scan"]: print("\nChecking Drive IDs against Internal Records")

		# Debug Output
		drive_map = session.query(Drive).filter_by(root_folder_id=root_folder_id).first()



		# Optional Output
		if output["drive_scan"]: print("\nLooking for 'N.I.T.E.':")
		
		# Scan Root Files for a matching title
		NITE_folder_id = check_files_for_title(files=root_files, title="N.I.T.E.")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was found with ID: {NITE_folder_id}\n")
		



		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'D.A.E.':")
		
		# Scan Root Files for a matching title
		DAE_folder_id = check_files_for_title(files=root_files, title="D.A.E.")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was found with ID: {DAE_folder_id}\n")

		



		# Scan DAE Folder
		DAE_files = query_drive(f"'{DAE_folder_id}' in parents")

		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Archive':")
		
		# Scan Root Files for a matching title
		archive_folder_id = check_files_for_title(files=DAE_files, title="Archive")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was found with ID: {archive_folder_id}\n")




		# Scan NITE Folder
		NITE_files = query_drive(f"'{NITE_folder_id}' in parents")

		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Evidence':")
		

		# Scan for Data Collection Folder
		data_collection_folder_id = check_files_for_title(files=NITE_files, title="Data Collection")["id"]
		data_collection_files = query_drive(f"'{data_collection_folder_id}' in parents")

		# Scan for Evidence Folder
		evidence_folder_id = check_files_for_title(files=data_collection_files, title="Evidence")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was found with ID: {evidence_folder_id}\n")



		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Current Events':")
		
		# Scan Root Files for a matching title
		current_events_file_id = check_files_for_title(files=NITE_files, title="Current Events")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was Found with ID: {current_events_file_id}\n")


		# Optional Output		
		if output["drive_scan"]: print("\nLooking for 'Templates':")
		
		# Scan Root Files for a matching title
		template_folder_id = check_files_for_title(files=DAE_files, title="Templates")["id"]
		
		# Optional Output
		if output["drive_scan"]: print(f"\tFile was found with ID: {template_folder_id}\n")

		


		# Iternalize the IDs of the required drive folders
		scanned_drive_map = Drive(template_folder_id=template_folder_id, root_folder_id=root_folder_id, NITE_folder_id=NITE_folder_id, DAE_folder_id=DAE_folder_id, archive_folder_id=archive_folder_id, evidence_folder_id=evidence_folder_id, current_events_file_id=current_events_file_id)
		
		if ((drive_map.template_folder_id != scanned_drive_map.template_folder_id) or (scanned_drive_map.root_folder_id != drive_map.root_folder_id) or (scanned_drive_map.NITE_folder_id != NITE_folder_id) or (scanned_drive_map.DAE_folder_id != drive_map.DAE_folder_id) or (scanned_drive_map.archive_folder_id != drive_map.archive_folder_id) or (scanned_drive_map.evidence_folder_id != drive_map.evidence_folder_id) or (scanned_drive_map.current_events_file_id != drive_map.current_events_file_id)):
			print("WARNING - THE FILESYSTEM SCANNED DOES NOT MATCH THE INTERNAL DATABASE")
		else:
			# Optional Output
			if output["drive_scan"]: print(f"\n Drive has been Validated:\n\t{drive_map}\n")





	if output: print(f"""\nDRIVE SUCCESSFULLY SCANNED\n#####################################################\n""")


# Validate Cloud Integrity
def validate_cloud_integrity():
	# Non-Optional Output
	if output: print(f"""\n#####################################################\nVALIDATING CLOUD INTEGRITY\n""")

	# Variables
	archive_folder_id = session.query(Drive).first().archive_folder_id
	status_of_cloud_files = "100%"

	##### WORKSPACE
	for event in session.query(Event).all():
		print(f"\n\nValidating Event: {event.title}\n\tYear Folder ID: {event.year_id}\n\tMonth Folder ID: {event.month_id}\n\tDay Folder ID: {event.day_id}\n\tEvent Folder ID: {event.drive_event_folder_id}\n\tArchive Folder ID: {event.drive_archive_folder_id}")
		
		# Check archive folder for the expected year folder
		year_exists_on_drive = check_files_for_id(files=list_drive_directory(id=archive_folder_id), id=event.year_id)

		# Check for Corrupted Events
		if event.year_id == None:
			pass


		if year_exists_on_drive:

			# Optional Output
			if output["cloud_integrity_check"]: print(f"{event.year} Validated Successfully")

			# Check year folder for the expected month folder
			month_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.year_id), id=event.month_id)

			if month_exists_on_drive:

				# Optional Output
				if output["cloud_integrity_check"]: print(f"{event.month} Validated Successfully")

				# Check month folder for the expected day folder
				day_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.month_id),id=event.day_id)

				if day_exists_on_drive:


					# Optional Output
					if output["cloud_integrity_check"]: print(f"{event.day} Validated Successfully")

					#Check day folder for the expected event folder
					event_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.day_id),id=event.drive_event_folder_id)

					if event_exists_on_drive:

						# Optional Output
						if output["cloud_integrity_check"]: print(f"\t{event.title} Has a Valid Event Folder")

						archive_folder_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.drive_event_folder_id),id=event.drive_archive_folder_id)

						if archive_folder_exists_on_drive:

							# Optional Output
							if output["cloud_integrity_check"]: print(f"\t{event.title} Has a Valid Archive Folder")

							text_folder_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.drive_archive_folder_id), id=event.drive_archive_text_folder_id)
							image_folder_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.drive_archive_folder_id), id=event.drive_archive_image_folder_id)
							video_folder_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.drive_archive_folder_id), id=event.drive_archive_video_folder_id)
							audio_folder_exists_on_drive = check_files_for_id(files=list_drive_directory(id=event.drive_archive_folder_id), id=event.drive_archive_audio_folder_id)
							all_folders_exist_in_archive = text_folder_exists_on_drive and image_folder_exists_on_drive and video_folder_exists_on_drive and audio_folder_exists_on_drive
							
							if all_folders_exist_in_archive:

								# Optional Output
								if output["cloud_integrity_check"]: print(f"\tArchive Folder Contains Required Folders")
								
								# Check text file
								text_file_exists = check_files_for_id(files=list_drive_directory(id=event.drive_archive_text_folder_id), id=event.drive_archive_text_file_id)

								if text_file_exists:
									# Optional Output
									if output["cloud_integrity_check"]: print(f"\tText File Verified")
									
									# Check Image Folder for Known Files
									for file in event.drive_archive_image_files_id_list:

										#image_file_found = check_files_for_id(files=list_drive_directory(id=event.drive_archive_image_folder_id), id=file)
										
										if not check_files_for_id(files=list_drive_directory(id=event.drive_archive_image_folder_id), id=file):
											# Optional Output
											if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.title} IS CORRUPTED")

											status_of_cloud_files = "Compromised - Attempting to Fix"

											# Set event.drive_archive_folder_id to null
											event.event_summary_file = ""

										else:
											# Optional Output
											if output["cloud_integrity_check"]: print(f"\tImage Files Verified")


									# Check Video Folder for Known Files
									for file in event.drive_archive_video_files_id_list:
										if not check_files_for_id(files=list_drive_directory(id=event.drive_archive_video_folder_id), id=file):
											# Optional Output
											if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.title} IS CORRUPTED")

											status_of_cloud_files = "Compromised - Attempting to Fix"

											# Set event.drive_archive_folder_id to null
											event.event_summary_file = ""

										else:
											# Optional Output
											if output["cloud_integrity_check"]: print(f"\tVideo Files Verified")


									# Check Audio Folder for Known Files
									for file in event.drive_archive_audio_files_id_list:
										if not check_files_for_id(files=list_drive_directory(id=event.drive_archive_audio_folder_id), id=file):
											# Optional Output
											if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.title} IS CORRUPTED")

											status_of_cloud_files = "Compromised - Attempting to Fix"

											# Set event.drive_archive_folder_id to null
											event.event_summary_file = ""

										else:
											# Optional Output
											if output["cloud_integrity_check"]: print(f"\t Audio Files Verified")
											

									# VERIFY FORMATTED MEDIA FILE LOCATIONS

								# ARCHIVE CORRUPTED - Reconstruction Required
								else:
									# Optional Output
									if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.title} IS CORRUPTED")

									status_of_cloud_files = "Compromised - Attempting to Fix"

									# Set event.drive_archive_folder_id to null
									event.event_summary_file = ""


							# ARCHIVE CORRUPTED - Reconstruction Required
							else:
								# Optional Output
								if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.title} IS CORRUPTED")

								status_of_cloud_files = "Compromised - Attempting to Fix"

								# Set event.drive_archive_folder_id to null
								event.event_summary_file = ""

							# CONFIRM SUMMARY DOCUMENTS AT A LATER TIME - IF MISSING, RECONSTRUCT EVENT

						# ARCHIVE MISSING - Reconstruction Required
						else:

							# Optional Output
							if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.title} IS CORRUPTED")

							status_of_cloud_files = "Compromised - Attempting to Fix"

							# Set event.drive_archive_folder_id to null
							event.event_summary_file = ""

					# EVENT DELETED - Reconstruction Required
					else:

						# Optional Output
						if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.title} COULD NOT BE LOCATED")

						status_of_cloud_files = "Compromised - Attempting to Fix"

						# Set event.drive_archive_folder_id to null
						event.event_summary_file = ""

				# DAY DELETED - Surgery Required
				else:

					# Optional Output
					if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.day} COULD NOT BE LOCATED")

					status_of_cloud_files = "Compromised - Attempting to Fix"

					# Delete event.drive_archive_folder_id - this will flag the event as new and re-generate it
					event.event_summary_file = ""

					# Delete broken entries
					session.delete(event.day)
					session.commit()

			# MONTH DELETED - Reconstructive surgery required
			else:

				# Optional Output
				if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.month} COULD NOT BE LOCATED")

				status_of_cloud_files = "Compromised - Attempting to Fix"

				# Delete event.drive_archive_folder_id - this will flag the event as new and re-generate it
				event.event_summary_file = ""

				# Delete broken entries
				if event.month != None:
					for day in event.month.days:
						session.delete(day)
					session.delete(event.month)
					session.commit()


		# YEAR DELETED - Massive reconstructive surgery required
		else:

			# Optional Output
			if output["cloud_integrity_check"]: print(f"\t\tWARNING: {event.year} COULD NOT BE LOCATED")

			status_of_cloud_files = "Compromised - Attempting to Fix"

			# Delete event.drive_archive_folder_id - this will flag the event as new and re-generate it
			event.event_summary_file = ""

			# Delete broken entries
			if event.year != None:
				months = session.query(Month).all()
				for month in event.year.months:
					for day in month.days:
						session.delete(day)
					session.delete(month)
				session.delete(event.year)
				session.commit()


	# Optional Output
	if output["cloud_integrity_check"]: print(f"\nCloud Status: {status_of_cloud_files}")

	# Non-Optional Output
	if output: print(f"""\nCLOUD INTEGRITY CHECK COMPLETED\n#####################################################\n""")


# Validate Database
def identify_new_events():
	
	# Non-Optional Output
	if output: print(f"""\n#####################################################\nIDENTIFYING NEW EVENTS\n""")

	# Initialize Variables
	new_events = []

	# Determine which events are new
	for event in session.query(Event).all():
		if not event.event_summary_file:
			new_events.append(event)

			# Optional Output
			if output["new_events"]: print(f"""New Event Detected: {event.title}""")

	# Non-Optional Output
	if output: print(f"""\nEVENTS IDENTIFIED SUCCESSFULLY\n#####################################################\n""")

	# Return New Events
	if len(new_events) < 1: new_events = None
	return new_events


# Upload new events to drive & generate/update their summary files
def archive_events(new_events):

	# Non-Optional Output
	if output: print(f"""\n#####################################################\nARCHIVING NEW EVENTS\n""")

	# Non-capitalized 'drive' is for reading while capitalized 'Drive' is for writing
	drive = session.query(Drive).first()

	# Archive new events
	for event in new_events:

		# Optional Output
		if output["new_events"]: print(f"""\nArchiving New Event""")
		
		# Identify Event
		title = event.title
		date = event.date

		# Optional Output
		if output["new_events"]: print(f"""\tTitle: {title}\n\tDate: {date}""")

		# Identify Date
		date = date.split("/")
		year = date[2]
		month = date[0]
		day = date[1]

		# Optional Output
		if output["new_events_plus"]: print(f"""\t\tyear = {year}\n\t\tmonth = {month}\n\t\tday = {day}""")




		# Check Database for Year
		year_exists = session.query(Year).filter_by(year=year).first()

		if year_exists:
			if output["new_events_plus"]: print(f"""\t\t\tThe Year '{year_exists.year}' Was found in the Internal Database""")
		else:
			if output["new_events_plus"]: print(f"""\t\t\tThe Year '{year}' Was not found in the Internal Database""")

			# Find Archive Folder
			archive_folder_id = drive.archive_folder_id

			# Scan Archive Folder
			year_files = query_drive(f"'{archive_folder_id}' in parents")

			# Scan Archive Folder for Matching Title
			year_exists_on_drive = check_files_for_title(files=year_files, title=year)
			if year_exists_on_drive:

				# Get Archive-Folder ID
				folder_id = year_exists_on_drive["id"]

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Year '{year}' was found on drive with ID: {folder_id}\n\t\t\tThe Year {year} has been added to the Internal Database.")

				# Add Year to Database
				add_to_db(Year(year=year, drive_folder_id=folder_id))
			else:

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Year '{year}' was not found on drive.\n\t\t\tCreating Year. . .")

				# Get Archive-Folder ID
				archive_folder_id = session.query(Drive).first().archive_folder_id
				
				# Add Year to Drive
				folder_id = create_drive_folder(id=archive_folder_id, title=year)

				# Add Year to Database
				add_to_db(Year(year=year, drive_folder_id=folder_id))

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Year '{year}' was created with ID: {folder_id}")
		
		# Determine the Correct Year
		year = session.query(Year).filter_by(year=year).first()

		# Optional Output
		if output["new_events"]: print(f"\t\t\tThe Year '{year.year}' Was Successfully Archived\n")




		# Check Database for Month
		month_exists = session.query(Month).filter_by(month=month, year_id=year.drive_folder_id).first()

		if month_exists:
			if output["new_events_plus"]: print(f"""\t\t\tThe Month {month_exists.month} Was found in the Internal Database""")
		else:
			if output["new_events_plus"]: print(f"""\t\t\tThe Month {month} Was not found in the Internal Database""")

			# Scan Year Folder
			month_files = query_drive(f"'{year.drive_folder_id}' in parents")

			# Scan Year Folder for Matching Title
			month_exists_on_drive = check_files_for_title(files=month_files, title=month)
			if month_exists_on_drive:

				# Get Month-Folder ID				
				folder_id = month_exists_on_drive["id"]
				
				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Month {month} was found on drive with ID: {folder_id}\n\t\t\tThe Month {month} has been added to the Internal Database.")

				# Add Month to Database
				add_to_db(Month(month=month, drive_folder_id=folder_id, year_id=year.drive_folder_id))
			else:

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Month {month} was not found on drive.\n\t\t\tCreating month. . .")

				# Add Month to Drive
				folder_id = create_drive_folder(id=year.drive_folder_id, title=month)

				# Add month to Database
				add_to_db(Month(month=month, drive_folder_id=folder_id, year_id=year.drive_folder_id))

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Month {month} was created with ID: {folder_id}")
		
		# Determine the Correct Month
		month = session.query(Month).filter_by(month=month, year_id=year.drive_folder_id).first()
		
		# Optional Output
		if output["new_events"]: print(f"\t\t\tThe Month {month.month} was Successfully Archived\n")




		# Check Database for Day
		day_exists = session.query(Day).filter_by(day=day, month_id = month.drive_folder_id, year_id=year.drive_folder_id).first()

		if day_exists:
			if output["new_events_plus"]: print(f"""\t\t\tThe Day {day_exists.day} Was found in the Internal Database""")
		else:
			if output["new_events_plus"]: print(f"""\t\t\tThe Day {day} Was not found in the Internal Database""")

			# Scan Month Folder
			day_files = query_drive(f"'{month.drive_folder_id}' in parents")

			# Optional Output
			if output["new_events_more"]: print(f" day_files: {day_files}")

			# Scan Month Folder for Matching Title
			day_exists_on_drive = check_files_for_title(files=day_files, title=day)
			if day_exists_on_drive:

				# Get Month-Folder ID
				folder_id = day_exists_on_drive["id"]

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Day {day} was found on drive with ID: {folder_id}\n\t\t\tThe Day {day} has been added to the Internal Database.")

				# Add Day to Database
				add_to_db(Day(day=day, drive_folder_id=folder_id, month_id=month.drive_folder_id, year_id=year.drive_folder_id))
			else:

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Day {day} was not found on drive.\n\t\t\tCreating day. . .")

				# Add Day to Drive
				folder_id = create_drive_folder(id=month.drive_folder_id, title=day)

				# Add Day to Database
				add_to_db(Day(day=day, drive_folder_id=folder_id, month_id=month.drive_folder_id, year_id=year.drive_folder_id))

				# Optional Output
				if output["new_events_plus"]: print(f"\t\t\tThe Day {day} was created with ID: {folder_id}")

		# Determine the Correct Day
		day = session.query(Day).filter_by(day=day, month_id=month.drive_folder_id, year_id=year.drive_folder_id).first()

		# Optional Output
		if output["new_events"]: print(f"\t\t\tThe Day {day.day} was Successfully Archived\n")



		# Optional Output
		if output["new_events_more"]: print(f"\t\tYear:\n\t\t\t{year}\n")
		if output["new_events_more"]: print(f"\t\tMonth:\n\t\t\t{month}\n")
		if output["new_events_more"]: print(f"\t\tDay:\n\t\t\t{day}\n")



		# Scan Day folder
		event_files = query_drive(f"'{day.drive_folder_id}' in parents")

		# Scan Day Folder for Matching Title
		event_exists_on_drive = check_files_for_title(files=event_files, title=event.title)
		if event_exists_on_drive:

			# Optional Output
			if output["new_events_plus"]: print(f"\t\t\tThe Event '{title}' was found on drive with ID: {event_exists_on_drive['id']}\n\t\t\tDeleting Old Event...")

			# Trash the old event
			delete_drive_folder(id=event_exists_on_drive['id'])

			#Optional Output
			if output["new_events_plus"]: print(f"\t\t\tOld Event Deleted Successfully. \n\t\t\tCreating New Event...")

			# Add Event to Database
			event.title=title 
			event.drive_event_folder_id=create_drive_folder(id=day.drive_folder_id, title=title)
			event.day_id=day.drive_folder_id
			event.month_id=month.drive_folder_id
			event.year_id=year.drive_folder_id

			session.commit()

		else:

			# Optional Output
			if output["new_events_plus"]: print(f"\t\t\tThe Event '{title}' was not found on drive.\n\t\t\tCreating event. . .")

			# Add Event to Drive
			event.title=title 
			event.drive_event_folder_id=create_drive_folder(id=day.drive_folder_id, title=title)
			event.day_id=day.drive_folder_id
			event.month_id=month.drive_folder_id
			event.year_id=year.drive_folder_id

			session.commit()

			# Optional Output
			if output["new_events_plus"]: print(f"\t\t\tThe Event '{title}' was created with ID: {event.drive_event_folder_id}")
		
		# Determine the Correct Event
		event = session.query(Event).filter_by(title=title, day_id=day.drive_folder_id, month_id=month.drive_folder_id, year_id=year.drive_folder_id).first()

		# Optional Output
		if output["new_events"]: print(f"\t\t\tThe Event '{title}' was Successfully Archived\n")



		## GENERATE EVENT SUMMARIES

		# Optional Output
		if output["new_events"]: print(f"\t\t\tScanning for Evidence pertaining to '{event.title}'")


		# Get current evidence
		evidence_folder_id = session.query(Drive).first().evidence_folder_id
		evidence_files = query_drive(f"'{evidence_folder_id}' in parents")
		evidence_list = []

		# Internalize Evidence from Event
		for link in event.evidence.split(","):
			id = link.split("open?id=")[1]
			evidence_list.append(check_files_for_id(files=evidence_files,id=id))


		# Optional Output
		if output["new_events_plus"] and (len(evidence_list) > 0): print(f"\t\t\tEvidence List Generated Successfully")
		elif output["new_events_plus"]: print(f"\t\t\tWARNING: Evidence List Failed to Generate")

		# Optional Output
		if output["new_events"]: print(f"\n\t\t\tCreating Archive Folder for '{event.title}'")

		# Create and Internalize the archive folder
		event.drive_archive_folder_id = create_drive_folder(id=event.drive_event_folder_id, title="Archive")
		session.commit()

		# Create and internalize the mimeType folders
		event.drive_archive_image_folder_id = create_drive_folder(id=event.drive_archive_folder_id, title="Images")
		event.drive_archive_text_folder_id = create_drive_folder(id=event.drive_archive_folder_id, title="Text")
		event.drive_archive_video_folder_id = create_drive_folder(id=event.drive_archive_folder_id, title="Video")
		event.drive_archive_audio_folder_id = create_drive_folder(id=event.drive_archive_folder_id, title="Audio")
		session.commit()

		# Optional Output
		if output["new_events_plus"]: print(f"\t\t\tArchive folder created with id: '{event.drive_archive_folder_id}'")

		# Optional Output
		if output["new_events"]: print(f"\n\t\t\tMoving Evidence into Event Archive")

		# Prepare evidence id collection (sorted by mimetype and stored in a mutablelist/pickletype)
		image_evidence_id_list = []
		video_evidence_id_list = []
		audio_evidence_id_list = []

		# Move evidence into archive by MIME Type
		for file in evidence_list:
			if file:
				file_title = file['title']			
				file_mimeType = file['mimeType'].split("/")[0]
				file_id = file['id']

				# Optional Output
				if output["new_events_plus"]: print(f"\n\tFILE TITLE: {file_title}\n\tFILE MIME: {file_mimeType}\n\tFILE ID: {file_id}")
				
				# Image Files
				if file_mimeType == "image":

					# Optional Output
					if output["new_events_plus"]: print(f"\nImage file '{file_title}' being moved...")

					# Copy File into Folder
					copy_id = copy_drive_file_to_folder(file_id=file_id, parent_id=event.drive_archive_image_folder_id, copy_title=file_title)
					
					# Collect Ids for validation
					image_evidence_id_list.append(copy_id)

					#Optional Output
					if output["new_events_more"]: print(f"\tNew File ID: {copy_id}")

				# Video Files
				if file_mimeType == "video":

					# Optional Output
					if output["new_events_plus"]: print(f"\nVideo file '{file_title}' being moved...")

					# Move File into Folder
					copy_id = copy_drive_file_to_folder(file_id=file_id, parent_id=event.drive_archive_video_folder_id, copy_title=file_title)
					
					# Collect Ids for validation
					video_evidence_id_list.append(copy_id)

					#Optional Output
					if output["new_events_more"]: print(f"\tNew File ID: {copy_id}")

				# Audio Files
				if file_mimeType == "audio":

					# Optional Output
					if output["new_events_plus"]: print(f"\nAudio file '{file_title}' being moved...")

					# Move File into Folder
					copy_id = copy_drive_file_to_folder(file_id=file_id, parent_id=event.drive_archive_audio_folder_id, copy_title=file_title)
					
					# Collect Ids for validation
					audio_evidence_id_list.append(copy_id)

					#Optional Output
					if output["new_events_more"]: print(f"\tNew File ID: {copy_id}")
		
		# Add Evidence ID Tags to database as a list
		event.drive_archive_image_files_id_list = image_evidence_id_list
		event.drive_archive_video_files_id_list = video_evidence_id_list
		event.drive_archive_audio_files_id_list = audio_evidence_id_list

		# Text Files - Optional Output
		if output["new_events"]: print(f"\n\nText file \"{event.title} - Text Summary.txt\" being generated...")
		
		#Optional Output
		if output["new_events_more"]: print(f"\n\t\tEvent Summary:\n\t\t\t'{event.summary}'")

		#Optional Output
		if output["new_events_more"]: print(f"\n\t\tText File Target Location:\n\t\t\t'{event.drive_archive_text_folder_id}'")


		# Generate Text File
		text_summary_id = create_drive_document(parent_id=event.drive_archive_text_folder_id, title="Text Summary.txt")
		insert_text_to_drive_document(id = text_summary_id, text=event.summary, index=1, font_size=16)
		event.drive_archive_text_file_id = text_summary_id
		session.commit()

		# Optional Output
		if output["new_events"]: print(f"Event Archived Successfully\n")

		# Optional Output
		if output["new_events"]: print(f"Compiling Media Files...\n")

		# Download Required Files
		download_drive_dir_files(id=event.drive_archive_image_folder_id)
		download_drive_dir_files(id=event.drive_archive_video_folder_id)
		download_drive_dir_files(id=event.drive_archive_audio_folder_id)

		# Optional Output
		if output["new_events"]: print(f"\nGenerating Audio Summary File...")

		# Generate Audio Summary File
		audio_summary_file = convert_text_to_audio_file(text=event.summary, directory=bot_workspace_location, file_name=f"{event.title} - Narrated Summary")

		# Optional Output
		if output["new_events"]: print(f"Uploading Audio Summary File...")

		# Upload Audio Summary File
		audio_summary_file_id = upload_file_to_drive(file=audio_summary_file, directory=bot_workspace_location, parent_id=event.drive_archive_audio_folder_id, file_name="Narrated Summary")

		# Optional Output
		if output["new_events"]: print(f"Updating Database...")

		# Update Database
		event.event_audio_summary_file = audio_summary_file_id
		session.commit()


		# Optional Output
		if output["new_events"]: print(f"\nGenerating Gif File...")


		# Prepare for Gif Generation
		length = determine_length_of_audio_file(file=bot_workspace_location + audio_summary_file)

		correct_files = []
		for file in os.listdir(bot_workspace_location):
			filename = file.split(".")[0]

			if filename in image_evidence_id_list:
				correct_files.append(file)

		# Generate Gif File
		if correct_files:
			gif_file = generate_gif_file(directory=bot_workspace_location, files=correct_files, file_name=f"{event.title} - Gif of Image Evidence", length=length, length_delay=3000)

			# Optional Output
			if output["new_events"]: print(f"Uploading Gif Summary File...")

			# Upload Gif File
			gif_file_id = upload_file_to_drive(file=gif_file, directory=bot_workspace_location, parent_id=event.drive_archive_image_folder_id, file_name="Gif of Image Evidence.gif")
			time.sleep(1)

			# Optional Output
			if output["new_events"]: print(f"Updating Database...")

			# Update Database
			event.event_gif_file = gif_file_id
			session.commit()


		# Optional Output
		if output["new_events"]: print(f"\nGenerating Audio File...")


		# Prepare for Audio File Generation
		correct_files = []
		for file in os.listdir(bot_workspace_location):
			filename = file.split(".")[0]

			if filename in audio_evidence_id_list:
				correct_files.append(file)

		# Generate Audio File
		if correct_files:
			audio_file = compile_audio_files(files=correct_files, directory=bot_workspace_location, file_name=f"{event.title} - Audio Evidence Compilation.mp3")

			# Optional Output
			if output["new_events"]: print(f"Uploading Audio File...")

			# Upload Audio File
			audio_file_id = upload_file_to_drive(file=audio_file, directory=bot_workspace_location, parent_id=event.drive_archive_audio_folder_id, file_name="Audio Evidence Compilation.mp3")


			# Optional Output
			if output["new_events"]: print(f"Updating Database...")

			# Update Database
			event.event_audio_file = audio_file_id
			session.commit()


		# Optional Output
		if output["new_events"]: print(f"\nGenerating Video File...")

		# Prepare for Video File Generation
		correct_files = []
		for file in os.listdir(bot_workspace_location):
			filename = file.split(".")[0]

			if filename in video_evidence_id_list:
				correct_files.append(file)


		# Generate Video File
		if correct_files:
			video_file = compile_video_files(files=correct_files, directory=bot_workspace_location, file_name=f"{event.title} - Video Evidence Compilation.mp4")


			# Optional Output
			if output["new_events"]: print(f"Uploading Video File...")


			# Upload Video File
			video_file_id = upload_file_to_drive(file=video_file, directory=bot_workspace_location, parent_id=event.drive_archive_video_folder_id, file_name="Video Evidence Compilation")


			# Optional Output
			if output["new_events"]: print(f"Updating Database...")

			# Update Database
			event.event_video_file = video_file_id
			session.commit()


		##### WORKSPACE #####

		# Optional Output
		if output["new_events"]: print(f"Generating Timeline Documents...")

		# Optional Output
		if output["new_events_more"]: print(f"Checking for pre-existing years document")		

		# Scan Archive Folder
		year_files = query_drive(f"'{drive.archive_folder_id}' in parents")

		# Verify Location of Years Document
		template_files = list_drive_directory(id=drive.template_folder_id)
		years_file_exists = check_files_for_title(files=year_files, title="Years")


		if years_file_exists:
			if drive.years_file_id == years_file_exists["id"]:

				# Optional Output
				if output["new_events"]: print(f"\nYears File Verified\n")

			# Years File Corrupted (To fix, delete and rebuild entire archive...)
			else:

				# Optional Output
				if output["new_events"]: print(f"\nYears File Could not be Verified - Generating a new one - NOTE: MANUAL REPAIRS NEEDED\n")

				delete_drive_folder(id=years_file_exists["id"])
				drive.years_file_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Years")["id"],copy_title="Years" , parent_id=drive.archive_folder_id)

				# Optional Output
				if output["new_events"]: print(f"\nYears File Generated\n")

		# Years File Missing
		else:
			# Optional Output
			if output["new_events"]: print(f"\nYears File Was Not Found - Generating a new one - NOTE: MANUAL REPAIRS NEEDED\n")

			drive.years_file_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Years")["id"], copy_title="Years", parent_id=drive.archive_folder_id)

			# Optional Output
			if output["new_events"]: print(f"\nYears File Generated\n")


		# Update the Database
		session.commit()


		# Check for Year Document
		year_files = list_drive_directory(id=event.year_id)
		year_file_exists = check_files_for_title(files=year_files, title=str(event.year.year) + " - Year Document")


		if year_file_exists:
			
			# Optional Output
			if output["new_events"]: print(f"Year File Found with id: {year_file_exists['id']}")
	
			if year_file_exists["id"] == event.year.document_id:
			
				# Optional output
				if output["new_events"]: print(f"Year File Verified Successfully")

			# Year Document is Corrupted
			else:
				# Optional output
				if output["new_events"]: print(f"Year File Could Not Be Verified - MANUAL PATCHING REQUIRED")

				# Delete The Corrupted File
				delete_drive_folder(id=year_file_exists["id"])

				# Create a New File
				event.year.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Year")["id"], copy_title=str(event.year.year) + " - Year Document", parent_id=event.year.drive_folder_id)
				session.commit()

				# Update Years Document
				insert_text_to_drive_document(id=drive.years_file_id, text=str(event.year.year), index=1, link="https://docs.google.com/document/d/" + event.year.document_id, font="Anonymous Pro", font_size=20)


		# If it doesn't exist, create it & Update the Database - ALSO ADD YEAR TO YEARS DOCUMENT
		else:

			# Optional output
			if output["new_events"]: print(f"Year File is Being Generated")

			# Create a New File
			event.year.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Year")["id"], copy_title=str(event.year.year) + " - Year Document", parent_id=event.year.drive_folder_id)
			session.commit()

			# Update Years Document
			insert_text_to_drive_document(id=drive.years_file_id, text=str(event.year.year), index=1, link="https://docs.google.com/document/d/" + event.year.document_id, font="Anonymous Pro", font_size=20)

		# Check for Month Document
		month_files = list_drive_directory(id=event.month_id)
		month_file_exists = check_files_for_title(files=month_files, title=str(event.month.month) + " - Month Document")


		if month_file_exists:
			
			# Optional Output
			if output["new_events"]: print(f"Month File Found with id: {month_file_exists['id']}")
	
			if month_file_exists["id"] == event.month.document_id:
			
				# Optional output
				if output["new_events"]: print(f"Month File Verified Successfully")

			# Month Document is Corrupted
			else:
				# Optional output
				if output["new_events"]: print(f"Month File Could Not Be Verified - MANUAL PATCHING REQUIRED")

				# Delete The Corrupted File
				delete_drive_folder(id=month_file_exists["id"])

				# Create a New File
				event.month.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Month")["id"], copy_title=str(event.month.month) + " - Month Document", parent_id=event.month.drive_folder_id)
				session.commit()

				# Update Years Document
				insert_text_to_drive_document(id=event.year.document_id, text=str(event.month.month), index=1, link="https://docs.google.com/document/d/" + event.month.document_id, font="Anonymous Pro", font_size=20)


		# If it doesn't exist, create it & Update the Database - ALSO ADD YEAR TO YEARS DOCUMENT
		else:

			# Optional output
			if output["new_events"]: print(f"Month File is Being Generated")

			# Create a New File
			event.month.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Month")["id"], copy_title=str(event.month.month) + " - Month Document", parent_id=event.month.drive_folder_id)
			session.commit()

			# Update Years Document
			insert_text_to_drive_document(id=event.year.document_id, text=str(event.month.month), index=1, link="https://docs.google.com/document/d/" + event.month.document_id, font="Anonymous Pro", font_size=20)


		# Check for Day Document
		day_files = list_drive_directory(id=event.day_id)
		day_file_exists = check_files_for_title(files=day_files, title=str(event.day.day) + " - Day Document")


		if day_file_exists:
			
			# Optional Output
			if output["new_events"]: print(f"Day File Found with id: {day_file_exists['id']}")
	
			if day_file_exists["id"] == event.day.document_id:
			
				# Optional output
				if output["new_events"]: print(f"Day File Verified Successfully")

			# Day Document is Corrupted
			else:
				# Optional output
				if output["new_events"]: print(f"Day File Could Not Be Verified - MANUAL PATCHING REQUIRED")

				# Delete The Corrupted File
				delete_drive_folder(id=day_file_exists["id"])

				# Create a New File
				event.day.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Day")["id"], copy_title=str(event.day.day) + " - Day Document", parent_id=event.day.drive_folder_id)
				session.commit()

				# Update Years Document
				insert_text_to_drive_document(id=event.month.document_id, text=str(event.day.day), index=1, link="https://docs.google.com/document/d/" + event.day.document_id, font="Anonymous Pro", font_size=20)


		# If it doesn't exist, create it & Update the Database - ALSO ADD YEAR TO YEARS DOCUMENT
		else:

			# Optional output
			if output["new_events"]: print(f"Day File is Being Generated")

			# Create a New File
			event.day.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Day")["id"], copy_title=str(event.day.day) + " - Day Document", parent_id=event.day.drive_folder_id)
			session.commit()

			# Update Years Document
			insert_text_to_drive_document(id=event.month.document_id, text=str(event.day.day), index=1, link="https://docs.google.com/document/d/" + event.day.document_id, font="Anonymous Pro", font_size=20)

		# Optional Output
		if output["new_events"]: print(f"Event File is Being Generated")


		print(f'https://drive.google.com/uc?id={str(event.event_gif_file)}')

		# Prepare for Event Document Generation
		template_id = check_files_for_title(files=template_files, title="Event")['id']
		requests = [


			##### LINKS

			# Hyperlink the Video Evidence
			{'updateTextStyle': {
			    'range': {
			        'startIndex': 111,
			        'endIndex': 120
			    },
			    'textStyle': {
			      'link': {'url': f"https://drive.google.com/drive/folders/{str(event.drive_archive_video_folder_id)}?usp=sharing"},
			      'weightedFontFamily': {
			        'fontFamily': "Times New Roman"},
			        'fontSize': {
			          'magnitude': 12,
			          'unit': 'PT'
			        },
			    },
			    'fields': 'link,weightedFontFamily,fontSize'
			  }
			},


			# Hyperlink the Audio Evidence
			{'updateTextStyle': {
			    'range': {
			        'startIndex': 101,
			        'endIndex': 111
			    },
			    'textStyle': {
			      'link': {'url': f"https://drive.google.com/drive/folders/{str(event.drive_archive_audio_folder_id)}?usp=sharing"},
			      'weightedFontFamily': {
			        'fontFamily': "Times New Roman"},
			        'fontSize': {
			          'magnitude': 12,
			          'unit': 'PT'
			        },
			    },
			    'fields': 'link,weightedFontFamily,fontSize'
			  }
			},

			# Hyperlink the Image Evidence
			{'updateTextStyle': {
			    'range': {
			        'startIndex': 91,
			        'endIndex': 101
			    },
			    'textStyle': {
			      'link': {'url': f"https://drive.google.com/drive/folders/{str(event.drive_archive_image_folder_id)}?usp=sharing"},
			      'weightedFontFamily': {
			        'fontFamily': "Times New Roman"},
			        'fontSize': {
			          'magnitude': 12,
			          'unit': 'PT'
			        },
			    },
			    'fields': 'link,weightedFontFamily,fontSize'
			  }
			},


			# Hyperlink the Archive
			{'updateTextStyle': {
			    'range': {
			        'startIndex': 39,
			        'endIndex': 55
			    },
			    'textStyle': {
			      'link': {'url': f"https://drive.google.com/drive/folders/{str(event.drive_event_folder_id)}?usp=sharing"},
			      'weightedFontFamily': {
			        'fontFamily': "Times New Roman"},
			        'fontSize': {
			          'magnitude': 12,
			          'unit': 'PT'
			        },
			    },
			    'fields': 'link,weightedFontFamily,fontSize'
			  }
			},

			# Hyperlink the Day
			{'updateTextStyle': {
			    'range': {
			        'startIndex': 30,
			        'endIndex': 37
			    },
			    'textStyle': {
			      'link': {'url': f"https://docs.google.com/document/d/{str(event.day.document_id)}"},
			      'weightedFontFamily': {
			        'fontFamily': "Times New Roman"},
			        'fontSize': {
			          'magnitude': 12,
			          'unit': 'PT'
			        },
			    },
			    'fields': 'link,weightedFontFamily,fontSize'
			  }
			},
			# Hyperlink the Month
			{'updateTextStyle': {
			    'range': {
			        'startIndex': 20,
			        'endIndex': 29
			    },
			    'textStyle': {
			      'link': {'url': f"https://docs.google.com/document/d/{str(event.month.document_id)}"},
			      'weightedFontFamily': {
			        'fontFamily': "Times New Roman"},
			        'fontSize': {
			          'magnitude': 12,
			          'unit': 'PT'
			        },
			    },
			    'fields': 'link,weightedFontFamily,fontSize'
			  }
			},


			# Hyperlink the Year
			{'updateTextStyle': {
			    'range': {
			        'startIndex': 11,
			        'endIndex': 19
			    },
			    'textStyle': {
			      'link': {'url': f"https://docs.google.com/document/d/{str(event.year.document_id)}"},
			      'weightedFontFamily': {
			        'fontFamily': "Times New Roman"},
			        'fontSize': {
			          'magnitude': 12,
			          'unit': 'PT'
			        },
			    },
			    'fields': 'link,weightedFontFamily,fontSize'
			  }
			},



			##### IMAGE

			{'insertInlineImage': {
				'location': {
					'index': 59
				},

			'uri': f'https://drive.google.com/uc?id={str(event.event_gif_file)}',
			
			'objectSize': {
				'height': {
					'magnitude': 250,
					'unit': 'PT'
				},
				'width': {
					'magnitude': 250,
					'unit': 'PT'
				}
			}}},

			##### TEXT

			# Add the Image Evidence
			{'replaceAllText': {
				'containsText': {
					'text': '{{IMAGE}}'}, 
				'replaceText': "Image Evidence"}			
			},


			# Add the Video Evidence
			{'replaceAllText': {
				'containsText': {
					'text': '{{VIDEO}}'}, 
				'replaceText': "Video Evidence"}			
			},


			# Add the Audio Evidence
			{'replaceAllText': {
				'containsText': {
					'text': '{{AUDIO}}'}, 
				'replaceText': "Audio Evidence"}			
			},


			# Add the Summary
			{'replaceAllText': {
				'containsText': {
					'text': '{{SUMMARY}}'}, 
				'replaceText': str(event.summary)}			
			},


			# Add the Archive
			{'replaceAllText': {
				'containsText': {
					'text': '{{EVENT_FOLDER}}'}, 
				'replaceText': "Filesystem"}			
			},


			# Add the Day
			{'replaceAllText': {
				'containsText': {
					'text': '{{DAY}}'}, 
				'replaceText': str(event.day.day)}			
			},


			# Add the Month
			{'replaceAllText': {
				'containsText': {
					'text': '{{MONTH}}'}, 
				'replaceText': str(event.month.month)}			
			},


			# Add the Year
			{'replaceAllText': {
				'containsText': {
					'text': '{{YEAR}}'}, 
				'replaceText': str(event.year.year)}			
			},


			# Add the Title
			{'replaceAllText': {
				'containsText': {
					'text': '{{TITLE}}'},
				'replaceText': str(event.title)}			
			},



			


			]
		# Create Event Document & Update the Database
		success = False
		while success != True:
			try:
				event.event_summary_file = create_document_from_template(template_id=template_id, batch_update=requests, target_directory=event.drive_event_folder_id, file_title=event.title)
				session.commit()
				success = True
			except:
				pass
				print("DOCS API FAILED - RETRYING")

		# Add Event to Day Document
		insert_text_to_drive_document(id=event.day.document_id, text=str(event.title), index=1, link="https://docs.google.com/document/d/" + event.event_summary_file, font="Anonymous Pro", font_size=20)

		# Optional Output
		if output["new_events"]: print(f"\nA Video Summary is being Generated")

		# Prepare to Generate Video
		video = f"{event.title} - Video Evidence Compilation.mp4"
		gif = f"{event.title} - Gif of Image Evidence.gif"
		gif_audio = f"{event.title} - Narrated Summary.mp3"
		audio = f"{event.title} - Audio Evidence Compilation.mp3"

		# Generate Video
		create_video(directory=bot_workspace_location, video=video, blank_png="blank.png", blank_video="blank.mp4", blank_video_directory=local_archive_folder_location, blank_png_directory=local_archive_folder_location,  audio=audio, gif=gif, gif_audio=gif_audio, file_name=f"{event.title} - Summary Video.mp4")

		# Upload Video & Update Database
		event.event_video_summary_file = upload_file_to_drive(file=f"{event.title} - Summary Video.mp4", directory=bot_workspace_location, parent_id=event.drive_archive_video_folder_id, file_name="Summary Video") 
		session.commit()
		

		# Optional Output
		if output["new_events"]: print(f"\nEvent has been archived Successfully!")

	# Non-Optional Output
	if output: print(f"""\nALL EVENTS ARCHIVED SUCCESSFULLY\n#####################################################\n""")


# Generate Timeline Videos
def generate_timeline_videos(new_videos):

	# Non-Optional Output
	if output: print(f"""\n#####################################################\nGENERATING NEW VIDEOS\n""")
	
	# Optional Output
	if output["generate_new_videos"]: print(f"Determining if Current Month has any Existing Day Videos")

	# Delete Current Month's Day's Video if needed
	for day in new_videos["current_month"].days:
		if day.video_folder_id:
			if output["generate_new_videos"]: print(f"Deleting a folder: {day.video_folder_id}")
			delete_drive_folder(id = day.video_folder_id)
			day.video_folder_id = None
			day.video_file = None
			session.commit()

			# Optional Output
			if output["generate_new_videos_more"]: print(f"Video Folder Found and Deleted Deleted")

	# Optional Output
	if output["generate_new_videos"]: print(f"Determining if Current Month has an Existing Video")

	# Delete Current Months's Video if needed
	current_month_video_folder = new_videos["current_month_video_folder"]
	if current_month_video_folder:
		if output["generate_new_videos"]: print(f"Deleting a folder: {current_month_video_folder}")
		delete_drive_folder(id=current_month_video_folder)
		new_videos['current_month'].video_folder_id = None
		new_videos['current_month'].video_file_id = None
		session.commit()

		# Optional Output
		if output["generate_new_videos_more"]: print(f"Video Folder Found and Deleted Deleted")


	# Optional Output
	if output["generate_new_videos"]: print(f"Determining if Current Year has an Existing Video")

	# Delete Current Year's Video if needed
	current_year_video_folder = new_videos["current_year_video_folder"]
	if current_year_video_folder:
		delete_drive_folder(id=current_year_video_folder)
		new_videos['current_year'].video_folder_id = None
		new_videos['current_year'].video_file_id = None
		session.commit()

		# Optional Output
		if output["generate_new_videos_more"]: print(f"Video Folder Found and Deleted Deleted")


	# Download Day Videos
	for day in new_videos["new_days"]:
		for event in day.events:

			# Optional Output
			if output["generate_new_videos_more"]: print(day, event.title, event.event_video_summary_file)

			download_drive_file(id=event.event_video_summary_file, file_name=f"{event.title}.mp4", directory=bot_workspace_location)

	# Build Day Videos
	for day in new_videos["new_days"]:

		current_day = str(day.day)
		events = day.events
		tmp = []
		for event in events:

			event_year = str(event.year.year)
			event_month = str(event.month.month)
			event_day = str(event.day.day)

			# Optional Output
			if output["generate_new_videos"]: print(f"{event.title} happened on {event_year}/{event_month}/{event_day}")

			tmp.append(event.title+".mp4")

		# Optional Output
		if output["generate_new_videos_more"]: print(tmp, "\n")

		day_video = compile_video_files(files=tmp, directory=bot_workspace_location, file_name=f"{event_year}-{event_month}-{event_day}.mp4")
		day.video_folder_id = create_drive_folder(id=day.drive_folder_id, title="Archive")
		day.video_id = upload_file_to_drive(file=day_video, directory=bot_workspace_location, parent_id=day.video_folder_id, file_name="Summary of the Day")

		session.commit()


	# Build Month Videos
	for month in new_videos["new_months"]:

		current_month = str(month.month)
		days = month.days
		tmp = []
		for day in days:

			current_year = str(day.year.year)
			current_month = str(day.month.month)
			current_day = str(day.day)

			# Optional Output
			if output["generate_new_videos"]: print(f"{current_day} has events in {current_year}/{current_month}")

			tmp.append(f"{current_year}-{current_month}-{current_day}.mp4")

		# Optional Output
		if output["generate_new_videos_more"]: print(tmp, "\n")

		month_video = compile_video_files(files=tmp, directory=bot_workspace_location, file_name=f"{event_year}-{event_month}.mp4")
		month.video_folder_id = create_drive_folder(id=month.drive_folder_id, title="Archive")
		month.video_id = upload_file_to_drive(file=month_video, directory=bot_workspace_location, parent_id=month.video_folder_id, file_name="Summary of the Month")

		session.commit()



	# Build Year Videos
	for year in new_videos["new_years"]:

		months = year.months
		tmp = []
		for month in months:

			current_year = str(month.year.year)
			current_month = str(month.month)

			# Optional Output
			if output["generate_new_videos"]: print(f"{current_month} has events in {current_year}")

			download_drive_file(id=month.video_id, file_name=f"{current_year}-{current_month}.mp4", directory=bot_workspace_location)
			tmp.append(f"{current_year}-{current_month}.mp4")

		# Optional Output
		if output["generate_new_videos_more"]: print(tmp, "\n")

		year_video = compile_video_files(files=tmp, directory=bot_workspace_location, file_name=f"{event_year}.mp4")		
		year.video_folder_id = create_drive_folder(id=year.drive_folder_id, title="Archive")
		year.video_id = upload_file_to_drive(file=year_video, directory=bot_workspace_location, parent_id=year.video_folder_id, file_name="Summary of the Year")

		session.commit()



	# Non-Optional Output
	if output: print(f"""\nNEW VIDEOS GENERATED\n#####################################################\n""")


# Identify which videos should be generated
def identify_new_videos():

	# Non-Optional Output
	if output: print(f"""\n#####################################################\nIDENTIFYING NEW VIDEOS\n""")


	# Optional Output
	if output["identify_new_videos"]: print(f"Determining Current Events")
	

	# Optional Output
	if output["identify_new_videos_more"]: print(f"Gathering All Years")


	# Get Years
	years =[]
	for year in session.query(Year).all():
		years.append(year)


	# Optional Output
	if output["identify_new_videos_more"]: print(f"Determining Current Year")


	# Get Current Year
	current_year = year
	for year in years:
		if int(year.year) > int(current_year.year):
			current_year = year


	# Optional Output
	if output["identify_new_videos_more"]: print(f"Gathering All Months")


	# Get Months
	months = []
	current_months = session.query(Year).filter_by(year=current_year.year).first().months
	for month in current_months:
		months.append(str(month.month))


	# Optional Output
	if output["identify_new_videos_more"]: print(f"Determining Current Month")


	# Get Current Month
	current_month = month
	for month in current_months:
		if int(month.month) > int(current_month.month):
			current_month = month


	# Optional Output
	if output["identify_new_videos_more"]: print(f"Initializing Current Month")


	# Get Current Month Video & Folder
	current_month_video = current_month.video_id
	current_month_video_folder = current_month.video_folder_id

	# Get Current Year Video & Folder
	current_year_video = current_year.video_id
	current_year_video_folder = current_year.video_folder_id


	# Optional Output
	if output["identify_new_videos_more"]: print(f"Current Month Initialized")


	# Optional Output
	if output["identify_new_videos"]: print(f"Current Month: {current_month}\nCurrent Month Video Folder: {current_month_video_folder}\nCurrent Month Video File: {current_month_video}")
	


	##### WORKSPACE

	# Optional Output
	if output["identify_new_videos"]: print(f"Determining New Videos")
	
	# Determine New Days
	new_days = []

	for day in current_month.days:
		if day.video_id:
			new_days.append(day)

	for day in session.query(Day).filter_by(video_id=None):
		new_days.append(day)

	# Determine New Months
	new_months = []
	if current_month.video_id: new_months.append(current_month)
	for month in session.query(Month).filter_by(video_id=None):
		new_months.append(month)

	# Determine New Years
	new_years = []
	if current_year.video_id: new_years.append(current_year)
	for year in session.query(Year).filter_by(video_id=None):
		new_years.append(year)

	# Optional Output
	if output["identify_new_videos"]: print(f"New Videos Found, Returning Results")



	# Format Data for Export
	new_videos = {
		'current_month' : current_month,
		'current_month_video' : current_month_video,
		'current_month_video_folder' : current_month_video_folder,
		'current_year' : current_year,
		'current_year_video' : current_year_video,
		'current_year_video_folder' : current_year_video_folder,
		'new_days' : new_days,
		'new_months' : new_months,
		'new_years' : new_years
	}


	# Optional Output
	if output["identify_new_videos_more"]: print(f"New Videos:\n{new_videos}")


	# Return 
	return new_videos


	# Non-Optional Output
	if output: print(f"""\nNEW VIDEOS IDENTIFIED\n#####################################################\n""")

# Clean the root directory (Prevents errors if crashed/interrupted during last run)
def initiate_automated_cleanup():

  # Non-Optional Output:
  if output: print(f"""\n#####################################################\nSTARTING CLEANUP SEQUENCE\n""")

  # Scan package root directory
  root_dir = os.fspath(pathlib.Path().parent.absolute())
  root_files = os.listdir(root_dir)

  # Scan package workspace directory
  workspace_files = os.listdir(bot_workspace_location)

  # Optional Output
  if output["cleanup_sequence"]: print(f"""
      root_dir: {root_dir}
      root_files: {root_files}

      workspace_dir: {bot_workspace_location}
      workspace_files: {workspace_files}
    """)


  # Optional Output
  if output["cleanup_sequence"]: print(f"\nCleaning Root Location Now...\n")

  for file in root_files:
    if file not in ["dae", "run.py", "readme.txt", "requirements.txt", ".gitignore", ".gitattributes", ".git", "Todo.txt"]:
      os.remove(file) # Delete the file

    # Optional Output
      if output["cleanup_sequence"]: print(f"{file} Was Deleted")
    else:
      if output["cleanup_sequence"]: print(f"{file} Was Detected")


  # Optional Output
  if output["cleanup_sequence"]: print(f"\nCleaning Bot Workspace Location Now...\n")

  for file in workspace_files:
    os.remove(os.path.join(bot_workspace_location, file)) # Delete the file

    # Optional Output
    if output["cleanup_sequence"]: print(f"{file} Was Deleted")




  if output: print(f"""\nCLEANUP SUCCESSFUL\n#####################################################\n""")

# Get current events and clean them for internalization
def get_current_events():

  # Non-Optional Output:
  if output: print(f"""\n#####################################################\nACQUIRING CURRENT EVENTS\n""")

  # Initialize Variables
  internalized_events = []
  current_events_file_id = session.query(Drive).first().current_events_file_id

  # Get current events
  current_events = requests.get(f"https://docs.google.com/spreadsheets/d/{current_events_file_id}/export?format=csv&id=1wbcY8SdHHHkZd-pg6cQjMm1o0xQZ8TsAWaO5jf31DJs&gid=1623064726").content.splitlines()[2:]
  
  # Optional Output
  if output["dirty_current_events"]: print(f"""\n
      Dirty Current Events:

        {current_events}
    
    """)
  
  # Clean and internalize current events
  for event in current_events:
    event = event.decode("UTF-8").replace("\"", "").split("'")

    # Optional Output
    if output["cleaner_actions"]: print(f"""\n
        NOW CLEANING 
    
          {event}
    
      """)

    # Clean the event
    for i in event:
      if i in [",", " ", ""]:
        event.remove(i)

    # Optional Output
        if output["cleaner_actions"]:print(f"An Event was Cleaned: {i} Was Removed")
    if output["clean_current_events"]: print(f"""\n
        Clean Current Events: 
          {current_events}
      """)

    # If the event is formatted correctly, internalize it
    if len(event) == 4:
      ## Variable Initialization
      # Standard Data
      standard_data = event[0].split(",")

      # Meta Information
      archived_on = standard_data[0]
      archived_by = standard_data[1]

      # Event Information
      date = standard_data[2]
      title = standard_data[3]

      # Non-Standard data
      non_standard_data = event[0:]

      tags = non_standard_data[1]
      evidence = non_standard_data[2]
      summary = non_standard_data[3]

      if title:

	      # Optional Output
	      if output["event_internalization"]:
	        print(f"""
	            {title} Was Scanned Correctly

	              -- META --
	                Archived on: {archived_on}
	                Archived by: {archived_by}
	              
	              -- STANDARD --
	                Date: {date}
	                Title: {title}

	              -- NON-STANDARD --
	                Tags: {tags}
	                Evidence: {evidence}
	                Summary: {summary}
	          """)

	      # Add event to list of internalized events
	      internalized_events.append(Event(archived_on=archived_on, archived_by=archived_by, date=date, title=title, tags=tags, evidence=evidence, summary=summary))

	      # Optional output
	      if output["event_internalization"]: print(f"{title} Internalized Successfully . . . ")
	    

    elif output["event_internalization"]: print(f"Incorrect Formatting: {event}")


  # Non-Optional Output:
  if output: print(f"""\nCURRENT EVENTS SUCCESSFULLY ACQUIRED\n#####################################################\n""")

  # Return Current Events
  return internalized_events

# Add current events to the database
def update_database(current_events):
  if output: print(f"""\n#####################################################\nUPDATING DATABASE\n""")

  for event in current_events:
    if not session.query(Event).filter_by(date=event.date, title=event.title).first():
      add_to_db(event)

    # Optional Output
      if output["database_update"]: print(f"'{event.title}' Was Added to the Internal Database")
    elif output["database_update"]: print(f"'{event.title}' Already Exists in the Internal Database")

  if output: print(f"""\nDATABASE SUCCESSFULLY UPDATED\n#####################################################\n""")


###########################################################################################################################################
##################################################### Models ##############################################################################
########################################################################################################################################### 
# Root Drive Model
class Drive(Base):
	__tablename__ = "Drive"
	root_folder_id = Column(String, primary_key=True, unique=True)
	NITE_folder_id = Column(String, unique=True)
	evidence_folder_id = Column(String, unique=True)
	DAE_folder_id = Column(String, unique=True)
	archive_folder_id = Column(String, unique=True)
	current_events_file_id = Column(String, unique=True)
	years_file_id = Column(String, unique=True)
	template_folder_id = Column(String, unique=True)

# Year Model
class Year(Base):
	__tablename__ = "Year"
	# Drive Information
	drive_folder_id = Column(String, primary_key=True)

	# Timeline 
	year = Column(Integer, unique=True)
	months = relationship("Month", backref="year")
	days = relationship("Day", backref="year")
	events = relationship("Event", backref="year")

	# Data
	document_id = Column(String)
	video_folder_id = Column(String)
	video_id = Column(String)

# Month Model
class Month(Base):
	__tablename__ = "Month"
	# Drive Information
	drive_folder_id = Column(String, primary_key=True)

	# Timeline
	year_id = Column(Integer, ForeignKey('Year.drive_folder_id'))
	month = Column(Integer)
	days = relationship("Day", backref="month")
	events = relationship("Event", backref="month")

	# Data
	document_id = Column(String)
	video_folder_id = Column(String)
	video_id = Column(String)

# Day Model
class Day(Base):
	__tablename__ = "Day"
	# Drive Information
	drive_folder_id = Column(String, primary_key=True)

	# Timeline 
	year_id = Column(Integer, ForeignKey('Year.drive_folder_id'))
	month_id = Column(Integer, ForeignKey('Month.drive_folder_id'))
	day = Column(Integer)
	events = relationship("Event", backref="day")

	# Data
	document_id = Column(String)
	video_folder_id = Column(String)
	video_id = Column(String)

# Event Model
class Event(Base):
	__tablename__ = "Event"
	id = Column(Integer, primary_key=True)

	# Timeline
	year_id = Column(Integer, ForeignKey('Year.drive_folder_id'))
	month_id = Column(Integer, ForeignKey('Month.drive_folder_id'))
	day_id = Column(Integer, ForeignKey('Day.drive_folder_id'))


	# Drive  Information
	drive_event_folder_id = Column(String())
	drive_archive_folder_id = Column(String())

	# Archive mimeType folders
	drive_archive_image_folder_id = Column(String())
	drive_archive_text_folder_id = Column(String())
	drive_archive_video_folder_id = Column(String())
	drive_archive_audio_folder_id = Column(String())

	# Source Evidence Files
	drive_archive_image_files_id_list = Column(MutableList.as_mutable(PickleType),default=[])
	drive_archive_video_files_id_list = Column(MutableList.as_mutable(PickleType),default=[])
	drive_archive_audio_files_id_list = Column(MutableList.as_mutable(PickleType),default=[])
	drive_archive_text_file_id = Column(String())

	# Formatted Media Files
	event_summary_file = Column(String())
	event_gif_file = Column(String())
	event_video_file = Column(String())
	event_audio_file = Column(String())
	event_audio_summary_file = Column(String())
	event_video_summary_file = Column(String())


	# Meta Information
	archived_on = Column(String())
	archived_by = Column(String())

	# Standard Information
	date = Column(String())
	title = Column(String())

	# Non-Standard Information
	evidence = Column(String())
	tags = Column(String())
	summary = Column(String())


###########################################################################################################################################
##################################################### Commands ############################################################################
###########################################################################################################################################

# Help
@dae.command()
async def help(ctx):
	# Output formatting
	embed = discord.Embed()
	embed.add_field(name="__Project Samsara__", value ="Welcome to Project Samsara! For help with my commands, please visit this link:", inline = False)
	embed.add_field(name="__Documentation__", value ="https://tinyurl.com/samsaradocumentation", inline = False)

	# Return
	await ctx.send(embed=embed)

# Home
@dae.command()
async def home(ctx):
	# Output formatting
	embed = discord.Embed()
	embed.add_field(name="__Project Samsara__", value =f"Welcome Back {ctx.message.author.mention}", inline = False)
	embed.add_field(name="__Project 107__", value ="https://tinyurl.com/samsarahome", inline = False)

	# Return
	await ctx.send(embed=embed)

# Encode Hels
@dae.command()
async def encode(ctx, clearText=None, alphaKey=None, keys=None):

	if (clearText and alphaKey and keys):
		# Variable Initialization
		alphabet = p108.create_alphabet(alphaKey)
		clearText = p108.clean_text(clearText.lower(), alphabet)
		encodeKeys = p108.clean_text(keys.replace(" ", "~"), alphabet).replace("~", " ")

		# Encryption	
		cipherText = p108.encode_hels(alphabet, encodeKeys.split(), clearText)

		# Output formatting
		embed = discord.Embed()
		embed.add_field(name="__Cleartext__:", value = "*" + clearText + "*", inline = False)
		embed.add_field(name="__Alphabet__:", value = "*" + "".join(alphabet) + "*", inline = False)
		embed.add_field(name="__Keys__:", value = "*" + keys + "*", inline=False)
		embed.add_field(name="__Ciphertext__:", value = "*" + cipherText + "*", inline = False)	

		# Return
		await ctx.send(embed=embed)
	else:
		
		# Output Formatting
		embed = discord.Embed()
		embed.add_field(name="__ERROR__:", value = "Please format your command like this:\n\n !encode 'cleartext' 'alphakey' 'keys'", inline = False)

		# Return
		await ctx.send(embed=embed)


# Decode Hels
@dae.command()
async def decode(ctx, cipherText=None, alphaKey=None, keys=None):

	if (cipherText and alphaKey and keys):
		# Variable Initialization
		alphabet = p108.create_alphabet(alphaKey)
		cipherText = p108.clean_text(cipherText.lower(), alphabet)
		decodeKeys = p108.clean_text("~".join(reversed(keys.split())), alphabet).replace("~", " ")

		# Decryption	
		clearText = p108.decode_hels(alphabet, decodeKeys.split(), cipherText)

		# Output Formatting
		embed = discord.Embed()
		embed.add_field(name="__Ciphertext__:", value = "*" + cipherText + "*", inline = False)
		embed.add_field(name="__Alphabet__:", value = "*" + "".join(alphabet) + "*", inline = False)
		embed.add_field(name="__Keys__:", value = "*" + keys + "*", inline=False)
		embed.add_field(name="__Cleartext__:", value = "*" + clearText + "*", inline = False)	

		# Return
		await ctx.send(embed=embed)
	else:

		# Output Formatting
		embed = discord.Embed()
		embed.add_field(name="__ERROR__:", value = "Please format your command like this:\n\n !encode 'ciphertext' 'alphakey' 'keys'", inline = False)

		# Return
		await ctx.send(embed=embed)

# Request Information on a particular timeframe
@dae.command()
async def index(ctx, timeframe="0000", event_title=None):

	# Parse User Input
	if timeframe:

		# Allow for !index usage on it's own
		year_override=False
		if timeframe == "0000": 
			timeframe_length = 0
		else:
			timeframe = timeframe.split("/")
			timeframe_length = len(timeframe)


		# Format the Input
		year, month, day = None, None, None
		year_exists, month_exists, day_exists = None, None, None
	

		# Query Database
		if timeframe_length > 0: 
			year = timeframe[0]
			year_exists = session.query(Year).filter_by(year=year).first()
	

		if timeframe_length > 1: 
			month = timeframe[1]
			month_exists = session.query(Month).filter_by(month=month).first()
	

		if timeframe_length > 2: 
			day = timeframe[2]
			day_exists = session.query(Day).filter_by(day=day).first()


		# Allow listing found events
		if event_title:
			event_exists = session.query(Event).filter_by(title=event_title).first()
		else:
			event_exists = False


		# Prepare the Output
		embed = discord.Embed()
		

		# Determine the correct data to output
		if year_exists: 
			if month_exists:
				if day_exists:
					if event_exists:
						requested_id = event_exists.event_video_summary_file
						event_summary_document = event_exists.event_summary_file
						event_tags = event_exists.tags

					# day
					else:
						requested_id = day_exists.document_id
						requested_video_id = month_exists.video_id
						found_data = session.query(Event).filter_by(day=day_exists).all()
						data_type = "event"

						export = []
						for found_event in found_data:
							export.append(found_event.title)

						found_data = export

				# Month
				else:
					requested_id = month_exists.document_id
					requested_video_id = month_exists.video_id
					found_data = session.query(Day).filter_by(month=month_exists).all()
					data_type = "day"

					export = []
					for found_day in found_data:
						export.append(str(found_day.day))

					found_data = export

			# Year
			else:
				requested_id = year_exists.document_id
				requested_video_id = year_exists.video_id
				found_data = session.query(Month).filter_by(year=year_exists).all()
				data_type = "month"

				export = []
				for found_month in found_data:
					export.append(str(found_month.month))

				found_data = export
		
		# None
		else:
			requested_id = False
			found_data = session.query(Year).all()
			data_type = "year"

			export = []
			for found_year in found_data:
				export.append(str(found_year.year))

			found_data = export


		# Determine which output to use
		# Event Data Found
		if event_exists:
			embed.add_field(
				name=f"*__Index__*",
				value=f"""
				{ctx.message.author.mention} has requested:
					\tYear: {year}
					\tMonth: {month}
					\tDay: {day}
					\tEvent: {event_title}
					\tTags: {event_tags}

				\nEvent Document:
				https://docs.google.com/document/d/{event_summary_document}

				\nSummary Video:
				https://drive.google.com/file/d/{requested_id}
			""")


		# Timeframe Data Found
		elif requested_id:
			embed.add_field(
				name=f"*__Index__*",
				value=f"""
				{ctx.message.author.mention} has requested: 
					\tYear: {year}
					\tMonth: {month}
					\tDay: {day}

				\n Here are the {data_type}s I found:
				{found_data}

				\nTimeline Document
				https://docs.google.com/document/d/{requested_id}

				\n Timeline Video
				https://drive.google.com/file/d/{requested_video_id}/view?usp=sharing
			""")


		# No Data Found
		else:
			if year:
				message = f"There are no events archived under the year {year}"
			else:
				message = ""

			embed.add_field(
				name=f"*__Index__*",
				value=f"""
				{message}

				\n Here are the years I found:
				{found_data}
			""")
		

		# Return
		await ctx.send(embed=embed)


# Return Current Events
@dae.command()
async def current_events(ctx):
	# Get all Years
	years = session.query(Year).all()

	# Get Current Year
	max_year = 0
	for year in years:
		if int(year.year) > int(max_year):
			current_year = year
			max_year = year.year

	# Get Current Month
	max_month = 0
	for month in current_year.months:
		if int(month.month) > max_month:
			current_month = month
			max_month = month.month

	# Gather the required resources
	requested_id = month.document_id
	requested_video_id = month.video_id
	days = []
	for day in month.days:
		days.append(day.day)

	# Prepare the output
	embed = discord.Embed()
	embed.add_field(
		name=f"*__Current Events__*",
		value=f"""
		{ctx.message.author.mention} has requested: 
			\tYear: {year.year}
			\tMonth: {month.month}

		\n Here are the days I found:
		{days}

		\nTimeline Document
		https://docs.google.com/document/d/{requested_id}

		\n Timeline Video
		https://drive.google.com/file/d/{requested_video_id}/view?usp=sharing
	""")

	# Return
	await ctx.send(embed=embed)

# Catch the user up
@dae.command()
async def catchmeup(ctx, timeframe=None):

	# Prepare the Output
	embed = discord.Embed()	

	if timeframe:

		# Format the Input
		timeframe = timeframe.split("/")
		timeframe_length = len(timeframe)
		year, month = None, None
		year_exists, month_exists = None, None
		if timeframe_length > 0: year = int(timeframe[0])
		if timeframe_length > 1: month = int(timeframe[1])

		# Get Current Year
		requested_year = session.query(Year).filter_by(year=year).first()
		if requested_year:
			if year == requested_year.year: 
				year_exists = True
				current_year = requested_year

		# Get Current Month
		if month:
			requested_month = session.query(Month).filter_by(month=month).first()
			if month == requested_month.month: 
				month_exists = True
				current_month = requested_month

		# Input Validation
		if year_exists:
			if month_exists:
				# Fetch remaining months of current year
				requested_months = []
				max_month = int(current_month.month)
				for month in current_year.months:
					if int(month.month) > max_month:
						requested_months.append(month)


			# Fetch the requested future years
			requested_years = []
			years = session.query(Year).all()
			for tmp_year in years:
				if tmp_year.year > year:
					requested_years.append(tmp_year)


			# Prepare the Output	
			if month_exists:
				embed.add_field(name=f"*__Catch Me Up__*",value=f"""{ctx.message.author.mention} has requested all new entries after (and including) {current_year.year}/{current_month.month}:""")
				embed.add_field(name=f"*__{current_year.year}/{current_month.month}__*",value=f"""
							\nTimeline Document
							https://docs.google.com/document/d/{current_month.document_id}

							\n Timeline Video
							https://drive.google.com/file/d/{current_month.video_id}/view?usp=sharing
					""")
				
				for month in requested_months:
					embed.add_field(name=f"*__{month.year.year}/{month.month}__*",value=f"""
							\nTimeline Document
							https://docs.google.com/document/d/{month.document_id}

							\n Timeline Video
							https://drive.google.com/file/d/{month.video_id}/view?usp=sharing
					""")

			else:
				embed.add_field(name=f"*__Catch Me Up__*",value=f"""{ctx.message.author.mention} has requested all new entries after (and including) {current_year.year}:""")
				embed.add_field(name=f"*__{current_year.year}__*",value=f"""
							\nTimeline Document
							https://docs.google.com/document/d/{current_year.document_id}

							\n Timeline Video
							https://drive.google.com/file/d/{current_year.video_id}/view?usp=sharing
					""")	


			for year in requested_years:
				embed.add_field(name=f"*__{year.year}__*",value=f"""
						\nTimeline Document
						https://docs.google.com/document/d/{year.document_id}

						\n Timeline Video
						https://drive.google.com/file/d/{year.video_id}/view?usp=sharing
				""")

			
		else:
			embed.add_field(name=f"*__Catch Me Up__*",value=f"""
						I could not find that year in my database
						Please use `!index` to explore the archives and try again with a valid timeframe
						""")
	else:
		embed.add_field(name=f"*__Catch Me Up__*",value=f"""
						Please use `!index` to explore the archives and try again with a valid timeframe
						""")
	# Return
	await ctx.send(embed=embed)


# Filter events by tag
@dae.command()
async def filter(ctx, tags=None):

	# Allows for use without tags
	if not tags:
		requested_events = None

		# Collect all known tags
		tags = []
		for event in session.query(Event).all():
			for tag in event.tags.replace(" ", "").split(","):
				if tag not in tags:
					tags.append(tag)

	else:


		tags = tags.split(",")
		events = session.query(Event).all()

		requested_events = []
		for event in events:

			# Initialize the filter (return only if all tags are found)
			number_of_tags = len(tags)
			number_of_matches = 0

			# Scan the event for matched tags
			for tag in tags:
				if tag in event.tags:
					number_of_matches += 1

			# Output the event if it contains the requested tags
			if number_of_matches == number_of_tags:
				requested_events.append(event)


	# Prepare Output
	embed = discord.Embed()
	if requested_events:
		for event in requested_events:
			embed.add_field(name=f"__{event.title}__", value=f"""
			\nTags: {event.tags}


			\nTimeline Document
			https://docs.google.com/document/d/{event.event_summary_file}

			\n Timeline Video
			https://drive.google.com/file/d/{event.event_video_summary_file}/view?usp=sharing

				""")
	else:
		embed.add_field(name=f"__Filter__", value=f"""
			\n To use filter, you must supply tags! Here are the tags I found:


			\n{tags}
				""")
			
			

	# Return
	await ctx.send(embed=embed)
