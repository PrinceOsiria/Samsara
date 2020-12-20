###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from samsara import *

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Clean the root directory (Prevents errors is crashed/interrupted during last run)
def initiate_automated_cleanup():

  # Non-Optional Output:
  if output: print(f"""
    #####################################################
    STARTING CLEANUP SEQUENCE""")

  # Scan package root directory
  root_dir = os.fspath(pathlib.Path().parent.absolute())
  root_files = os.listdir(root_dir)

  # Optional Output
  if output["cleanup_sequence"]: print(f"""
      root_dir: {root_dir}
      root_files: {root_files}
    """)

  for file in root_files:
    if file not in ["dae", "run.py", "README.md", ".gitignore", ".gitattributes", ".git"]:
      os.remove(file) # Delete the file

    # Optional Output
      if output["cleanup_sequence"]: print(f"{file} WAS DELETED DURING AN AUTOMATED CLEANUP SEQUENCE")
    else:
      if output["cleanup_sequence"]: print(f"{file} SUCCESSFULLY FOUND")

  if output: print(f"""
    CLEANUP SUCCESSFUL
    #####################################################""")

# Get current events and clean them for internalization
def get_current_events():

  # Non-Optional Output:
  if output: print(f"""
    #####################################################
    ACQUIRING CURRENT EVENTS""")

  # Initialize Variables
  internalized_events = []

  # Get current events
  current_events = requests.get("https://docs.google.com/spreadsheets/d/1wbcY8SdHHHkZd-pg6cQjMm1o0xQZ8TsAWaO5jf31DJs/export?format=csv&id=1wbcY8SdHHHkZd-pg6cQjMm1o0xQZ8TsAWaO5jf31DJs&gid=1623064726").content.splitlines()[2:]
  
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
        if output["cleaner_actions"]:print(f"AN EVENT WAS CLEANED: {i} WAS REMOVED")
    if output["clean_current_events"]: print(f"""\n
        Clean Current Events: 
          {current_events}
      """)

    # Optional output
    if output["event_internalization"]: print(f"Event of length {len(event)} is being Scanned . . . ")

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

      # Optional Output
      if output["event_internalization"]:
        print(f"""
            ["{title}"] WAS INTERNALIZED

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
      if output["event_internalization"]: print(f"Event of length {len(event)} Scanned successfully . . . ")
    

    elif output["event_internalization"]: print(f"INCORRECT FORMATTING: {event}")


  # Non-Optional Output:
  if output: print(f"""
    CURRENT EVENTS SUCCESSFULLY ACQUIRED
    #####################################################""")

  # Return Current Events
  return internalized_events

# Add current events to the database
def update_database(current_events):
  if output: print(f"""
    #####################################################
    UPDATING DATABASE""")

  for event in current_events:
    if not session.query(Event).filter_by(date=event.date, title=event.title).first():
      add_to_db(event)

    # Optional Output
      if output["database_update"]: print(f"'{event.title}' WAS ADDED TO THE INTERNAL DATABASE")
    elif output["database_update"]: print(f"'{event.title}' ALREADY EXISTS IN THE INTERNAL DATABASE")

  if output: print(f"""
    DATABASE SUCCESSFULLY UPDATED
    #####################################################""")


