###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
#Configuration
from dae.Config import private_key_location, bot_workspace_location
from dae.Config import root_folder_id as drive_root_folder_id

# Local Filesystem Configuration - DEUBUG ONLY
#private_key_location = "C:/Users/tyler/Documents/GitHub/Samsara/dae/Archive" + "/" + "private_key.json"
#bot_workspace_location = "C:/Users/tyler/Documents/GitHub/Samsara/dae/Archive/tmp/"
#drive_root_folder_id = "19gVNYWPR4B3h4CduKKKr2qmKUwc0gALK"

# Google Drive Access
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from googleapiclient.discovery import build
import google.auth


###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Authentication
gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(private_key_location, scope)
service = build('docs', 'v1', credentials=gauth.credentials)
drive = GoogleDrive(gauth)
docs = service.documents()

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
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


# This stupid shit must be run first - otherwise certain (if not all) api features will not work
query_drive(f"'{drive_root_folder_id}' in parents")


##### WORKSPACE #####
#requests = [{'replaceAllText': {'containsText': {'text': '{{ TITLE }}'},'replaceText': "Test 2 Passed",}}]
#create_document_from_template(template_id="1kJsiH2tddGPLEUPCcu0xoR7F9G60wMkCrTsjPK2WbDM", batch_update=requests, target_directory="1euXckytMrTz8t2wkBCkI-yBU0OCI4hJF", file_title="Test 1 Passed")
#insert_text_to_drive_document(id="1TY0luNcLqjJ4npCQ_bkeo3jXfEKqKY4f58d9MPi7hs4", text="2021", index=1, offset=5, link="https://www.example.com", font="Anonymous Pro", font_size=30)
