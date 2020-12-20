###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Query drive
def query_drive(query=None):
  if query:
    return drive.ListFile(dict(q = query)).GetList()

# Internalize files from filelist
def internalize_drive_file(file_list=None):

  # Get file title
  def get_title_from_drive_filelist(file_list=None):
    for file in file_list:
      if file["title"]:
        return file["title"]

  # Get file id
  def get_id_from_drive_filelist(file_list=None):
    for file in file_list:
      if file["id"]:
        return file["id"]

  # Get file mime
  def get_mime_from_drive_filelist(file_list=None):
    for file in file_list:
      if file["mimeType"]:
        return file["mimeType"]

  return dict(
    title = get_title_from_drive_filelist(file_list=file_list),
    id = get_id_from_drive_filelist(file_list=file_list),
    mimeType = get_mime_from_drive_filelist(file_list=file_list)
    )

# Download files given a dictionary with title and id pairings for files
def download_drive_files(file_list=None, debug=True):
  for file in file_list:

    # Identify files
    title = file["title"]
    id = file["id"]
    file_mime = file["mimeType"]

    # Download files
    files = query_drive(f"title = '{title}'")
    for dl in files:
      dl.GetContentFile(title)

      # Search events for an id-evidence match
      os.rename(title, id)
