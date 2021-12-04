###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
#Configuration
from dae.Config import private_key_location

# Google Drive Access
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
import google.auth

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Authentication
gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(private_key_location, scope)
drive = GoogleDrive(gauth)


###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Download Drive Files from Directory
def download_drive_dir_files(id=None):
  file_list = list_drive_directory(id)
  for i, file1 in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
      print('Downloading {} from GDrive ({}/{})'.format(file1['title'], i, len(file_list)))
      file1.GetContentFile(file1['title'])  


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
