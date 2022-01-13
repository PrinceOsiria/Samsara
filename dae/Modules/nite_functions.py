###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from dae import *
from dae.Config import root_folder_id, years_document_id, bot_workspace_location

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
				drive.years_file_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Years")["id"], copy_title="Years", parent_id=drive.archive_folder_id)

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
		year_file_exists = check_files_for_title(files=year_files, title=str(event.year.year))


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
				event.year.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Year")["id"], copy_title=event.year.year, parent_id=event.year.drive_folder_id)
				session.commit()

				# Update Years Document
				insert_text_to_drive_document(id=drive.years_file_id, text=str(event.year.year), index=1, link="https://docs.google.com/document/d/" + event.year.document_id, font="Anonymous Pro", font_size=20)


		# If it doesn't exist, create it & Update the Database - ALSO ADD YEAR TO YEARS DOCUMENT
		else:

			# Optional output
			if output["new_events"]: print(f"Year File is Being Generated")

			# Create a New File
			event.year.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Year")["id"], copy_title=event.year.year, parent_id=event.year.drive_folder_id)
			session.commit()

			# Update Years Document
			insert_text_to_drive_document(id=drive.years_file_id, text=str(event.year.year), index=1, link="https://docs.google.com/document/d/" + event.year.document_id, font="Anonymous Pro", font_size=20)

		# Check for Month Document
		month_files = list_drive_directory(id=event.month_id)
		month_file_exists = check_files_for_title(files=month_files, title=str(event.month.month))


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
				event.month.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Month")["id"], copy_title=event.month.month, parent_id=event.month.drive_folder_id)
				session.commit()

				# Update Years Document
				insert_text_to_drive_document(id=event.year.document_id, text=str(event.month.month), index=1, link="https://docs.google.com/document/d/" + event.month.document_id, font="Anonymous Pro", font_size=20)


		# If it doesn't exist, create it & Update the Database - ALSO ADD YEAR TO YEARS DOCUMENT
		else:

			# Optional output
			if output["new_events"]: print(f"Month File is Being Generated")

			# Create a New File
			event.month.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Month")["id"], copy_title=event.month.month, parent_id=event.month.drive_folder_id)
			session.commit()

			# Update Years Document
			insert_text_to_drive_document(id=event.year.document_id, text=str(event.month.month), index=1, link="https://docs.google.com/document/d/" + event.month.document_id, font="Anonymous Pro", font_size=20)


		# Check for Day Document
		day_files = list_drive_directory(id=event.day_id)
		day_file_exists = check_files_for_title(files=day_files, title=str(event.day.day))


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
				event.day.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Day")["id"], copy_title=event.day.day, parent_id=event.day.drive_folder_id)
				session.commit()

				# Update Years Document
				insert_text_to_drive_document(id=event.month.document_id, text=str(event.day.day), index=1, link="https://docs.google.com/document/d/" + event.day.document_id, font="Anonymous Pro", font_size=20)


		# If it doesn't exist, create it & Update the Database - ALSO ADD YEAR TO YEARS DOCUMENT
		else:

			# Optional output
			if output["new_events"]: print(f"Day File is Being Generated")

			# Create a New File
			event.day.document_id = copy_drive_file_to_folder(file_id=check_files_for_title(files=template_files, title="Day")["id"], copy_title=event.day.day, parent_id=event.day.drive_folder_id)
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
					'magnitude': 500,
					'unit': 'PT'
				},
				'width': {
					'magnitude': 500,
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
		event.event_summary_file = create_document_from_template(template_id=template_id, batch_update=requests, target_directory=event.drive_event_folder_id, file_title=event.title)
		session.commit()

		# Add Event to Day Document
		insert_text_to_drive_document(id=event.day.document_id, text=str(event.title), index=1, link="https://docs.google.com/document/d/" + event.event_summary_file, font="Anonymous Pro", font_size=20)

		# Optional Output
		if output["new_events"]: print(f"\nA Video Summary is being Generated")

		# Prepare to Generate Video
		video = f"{event.title} - Video Evidence Compilation.mp4"
		gif = f"{event.title} - Gif of Image Evidence.gif"
		gif_audio = f"{event.title} - Narrated Summary.mp3"

		# Generate Video
		create_video(directory=bot_workspace_location,video=video, gif=gif, gif_audio=gif_audio, file_name=f"{event.title} - Summary Video.mp4")

		# Upload Video & Update Database
		event.event_video_summary_file = upload_file_to_drive(file=f"{event.title} - Summary Video.mp4", directory=bot_workspace_location, parent_id=event.drive_archive_video_folder_id, file_name="Summary Video") 
		session.commit()
		

		# Optional Output
		if output["new_events"]: print(f"\nEvent has been archived Successfully!")

	# Non-Optional Output
	if output: print(f"""\nALL EVENTS ARCHIVED SUCCESSFULLY\n#####################################################\n""")

