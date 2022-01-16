###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Bot Imports
from dae import *

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
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
