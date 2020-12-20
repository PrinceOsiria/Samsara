###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
from dae import *

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################

# Query drive
def query_drive(query):
  return drive.ListFile(dict(q = query)).GetList()


# Get files in folder via id
def internalize_drive_folder(query):
    # Initialize variables
    files = []

    # For each child file
    for file in query:
      
      # Create a dictionary of identifying information
      files.append(dict(
          title = file["title"],
          id = file["id"],
          mimeType = file["mimeType"]
        ))

    # Return a list of those file dictionaries
    return files



# Download files given a dictionary with title and id pairings for files
def download_drive_files(file_list=None, debug=True):
  for file in file_list:

    # Identify files
    title = file["title"]
    id = file["id"]
    file_mime = file["mimeType"].split("/")

    # Download files
    files = query_drive(f"title = '{title}'")
    for dl in files:
      dl.GetContentFile(title) # Download a title via it's title
      os.rename(title, id) # Rename the file according to it's id
