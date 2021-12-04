###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from dae import *
from dae.Config import root_folder_id

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
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




		# Iternalize the IDs of the required drive folders
		drive_map = Drive(root_folder_id=root_folder_id, NITE_folder_id=NITE_folder_id, DAE_folder_id=DAE_folder_id, archive_folder_id=archive_folder_id, evidence_folder_id=evidence_folder_id, current_events_file_id=current_events_file_id)
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



		# Iternalize the IDs of the required drive folders
		scanned_drive_map = Drive(root_folder_id=root_folder_id, NITE_folder_id=NITE_folder_id, DAE_folder_id=DAE_folder_id, archive_folder_id=archive_folder_id, evidence_folder_id=evidence_folder_id, current_events_file_id=current_events_file_id)
		
		if ((scanned_drive_map.root_folder_id != drive_map.root_folder_id) or (scanned_drive_map.NITE_folder_id != NITE_folder_id) or (scanned_drive_map.DAE_folder_id != drive_map.DAE_folder_id) or (scanned_drive_map.archive_folder_id != drive_map.archive_folder_id) or (scanned_drive_map.evidence_folder_id != drive_map.evidence_folder_id) or (scanned_drive_map.current_events_file_id != drive_map.current_events_file_id)):
			print("WARNING - THE FILESYSTEM SCANNED DOES NOT MATCH THE INTERNAL DATABASE")
		else:
			# Optional Output
			if output["drive_scan"]: print(f"\n Drive has been Validated:\n\t{drive_map}\n")





	if output: print(f"""\nDRIVE SUCCESSFULLY SCANNED\n#####################################################\n""")


# Validate Cloud Integrity
def validate_cloud_integrity():

	# Variables
	status_of_cloud_files = "UNKNOWN"

	# Output
	if output: print(f"""\n#####################################################\nVALIDATING CLOUD INTEGRITY\n""")

	#For year in db


	# Optional Output
	if output["cloud_integrity_check"]: print(f"\n\nCloud Status: {status_of_cloud_files}")

	# Output
	if output: print(f"""\nCLOUD INTEGRITY CHECK COMPLETED\n#####################################################\n""")



# Validate Database
def identify_new_events():
	
	# Non-Optional Output
	if output: print(f"""\n#####################################################\nIDENTIFYING NEW EVENTS\n""")

	# Initialize Variables
	new_events = []

	# Determine which events are new
	for event in session.query(Event).all():
		if not event.drive_archive_folder_id:
			new_events.append(event)

			# Optional Output
			if output["new_events"]: print(f"""New Event Detected: {event.title}""")

	# Non-Optional Output
	if output: print(f"""\nEVENTS IDENTIFIED SUCCESSFULLY\n#####################################################\n""")

	# Return New Events
	return new_events


# Upload new events to drive & generate/update their summary files
def archive_events(new_events):

	# Non-Optional Output
	if output: print(f"""\n#####################################################\nARCHIVING NEW EVENTS\n""")

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
			archive_folder_id = session.query(Drive).first().archive_folder_id

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

					# Move File into Folder
					parents = move_drive_file(file_id=file_id, parent_id=event.drive_archive_image_folder_id)
					
					#Optional Output
					if output["new_events_more"]: print(f"\tFile Parent Folder: {parents}")

				# Video Files
				if file_mimeType == "video":

					# Optional Output
					if output["new_events_plus"]: print(f"\nVideo file '{file_title}' being moved...")

					# Move File into Folder
					parents = move_drive_file(file_id=file_id, parent_id=event.drive_archive_video_folder_id)
					
					#Optional Output
					if output["new_events_more"]: print(f"\tFile Parent Folder: {parents}")

				# Audio Files
				if file_mimeType == "audio":

					# Optional Output
					if output["new_events_plus"]: print(f"\nAudio file '{file_title}' being moved...")

					# Move File into Folder
					parents = move_drive_file(file_id=file_id, parent_id=event.drive_archive_audio_folder_id)
					
					#Optional Output
					if output["new_events_more"]: print(f"\tFile Parent Folder: {parents}")
				


##### WORKSPACE

		# Text Files - Optional Output
		if output["new_events"]: print(f"\n\n\tText file \"{event.title} - Text Summary.txt\" being generated...")
		
		#Optional Output
		if output["new_events_plus"]: print(f"\n\t\tEvent Summary:\n\t\t\t'{event.summary}'")

		#Optional Output
		if output["new_events_plus"]: print(f"\n\t\tText File Target Location:\n\t\t\t'{event.drive_archive_text_folder_id}'")





		# Optional Output
		if output["new_events"]: print(f"\n\nEvent Archived Successfully\n")

		# Optional Output
		if output["new_events"]: print(f"\n\n\nCompiling Media Files...\n")

	# Non-Optional Output
	if output: print(f"""\nEVENTS ARCHIVED SUCCESSFULLY\n#####################################################\n""")

