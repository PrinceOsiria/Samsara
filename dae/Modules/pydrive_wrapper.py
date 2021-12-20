###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
#Configuration
from dae.Config import private_key_location, bot_workspace_location

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
def download_drive_dir_files(id=None, file_identifier="File Number"):

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
  return file["parents"]



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
def insert_text_to_drive_document(id=None, text=None, index=1):

  content = [
    {'insertText': {
      'location': {'index': index},
      'text':text}
    }]

  docs.batchUpdate(documentId=id,body={'requests': content}).execute()


# Upload Files
def upload_file_to_drive(file=None, directory=None, parent_id=None, file_name=None):
  file1 = drive.CreateFile({'title': file_name})
  file1.SetContentFile(directory+file)
  file1.Upload()
  move_drive_file(file_id=file1['id'], parent_id=parent_id)
  return file1['id']





