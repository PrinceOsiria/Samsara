###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from dae import *
from dae.Archive.Model import *

# MIME Type Identification
import magic


###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Get this month's events from the shared sheet
def get_current_events():
	# Clean the root directory (Prevents errors is crashed/interrupted during last run)
	root_dir = os.fspath(pathlib.Path().parent.absolute())
	root_files = os.listdir(root_dir)
	for file in root_files:
		if file not in ["dae", "run.py"]:
			os.remove(file)

	# Download current events and stream it directly into the return to be parsed
	return requests.get("https://docs.google.com/spreadsheets/d/1wbcY8SdHHHkZd-pg6cQjMm1o0xQZ8TsAWaO5jf31DJs/export?format=csv&id=1wbcY8SdHHHkZd-pg6cQjMm1o0xQZ8TsAWaO5jf31DJs&gid=1623064726").content


# Generate Event Document Templates for Each Event
def generate_templates(debug=False):
	# For each year in cache
	cache_dir = (os.fspath(pathlib.Path().parent.absolute()) + f"\\dae\\Archive\\Cache\\")
	year_folders = os.listdir(cache_dir)
	for year_folder in year_folders:

		##### DEBUG
		if debug:
			print(f"""
					Cache Directory: {cache_dir}
					Year Folders: {year_folders}
					Current Year: {year_folder}
			""")	


		# for each month in year
		year_dir = cache_dir + f"{year_folder}\\"
		month_folders = os.listdir(year_dir)
		for month_folder in month_folders:

			##### DEBUG
			if debug:
				print(f"""
						Year Directory: {year_dir}
						Month Folders: {month_folders}
						Current Month: {month_folder}
					""")


			# for each day in month
			month_dir = year_dir + f"{month_folder}\\"
			day_folders = os.listdir(month_dir)
			for day_folder in day_folders:

				##### DEBUG
				if debug:
					print(f"""
							Month Directory: {month_dir}
							Day Folders: {day_folders}
							Current Day: {day_folder}
						""")


				# for each event in day
				day_dir = month_dir + f"{day_folder}\\"
				event_folders = os.listdir(day_dir)
				for event_folder in event_folders:


					##### DEBUG
					if debug:
						print(f"""
								Day Directory: {day_dir}
								Event Folders: {event_folders}
								Current Event: {event_folder}
							""")




					## Generate Template for Event Document
					# Identify Present File Types
					event_dir = day_dir + f"{event_folder}\\"
					type_folders = os.listdir(event_dir)



					# Add Images to template
					if "image" in type_folders:
						image_dir = event_dir+"image\\"
						image_files = os.listdir(image_dir)

						##### DEBUG
						if debug:
							print(f"""
									Image Directory: {image_dir}
									Image Files: {image_files}
								""")



					# Add summary to template
					if "text" in type_folders:
						text_dir = event_dir+"text\\"
						text_files = os.listdir(text_dir)

						##### DEBUG
						if debug:
							print(f"""
									Text Directory: {text_dir}
									Text Files: {text_files}
								""")



					# Add video to template
					if "video" in type_folders:
						video_dir = event_dir+"video\\"
						video_files = os.listdir(video_dir)

						##### DEBUG
						if debug:
							print(f"""
									Video Directory: {video_dir}
									Video Files: {video_files}
								""")



					# Add audio to template
					if "audio" in type_folders:
						audio_dir = event_dir+"audio\\"
						audio_files = os.listdir(audio_dir)

						##### DEBUG
						if debug:
							print(f"""
									Audio Directory: {audio_dir}
									Audio Files: {audio_files}
								""")





			


###########################################################################################################################################
##################################################### Tasks $##############################################################################
###########################################################################################################################################
# Task Practice
@tasks.loop(seconds=120)
async def validate_archive():
	# Initialize Variables
	standard_events = []

	# Get current events
	current_events = get_current_events().splitlines()[2:]

	# Parse current events for every individual event
	for event in current_events:
		event = event.decode("UTF-8").replace("\"", "").split("'")
		
		# Clean the event
		for i in event:
			if i in [",", " ", ""]:
				event.remove(i)

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

			standard_events.append(Event(archived_on=archived_on, archived_by=archived_by, date=date, title=title, tags=tags, evidence=evidence, summary=summary))


	# Duplicate Preventing Database Uploader
	for event in standard_events:
		if not len(session.query(Event).filter_by(date=date).all())>0:
			if not len(session.query(Event).filter_by(title=title).all())>0:
				add_to_db(event)
		
	
	# Gets root files and stores them in a nested dictionary which contains that files title and id
	Google_Drive = startup_drive()

	# Get evidence files
	evidence_files = get_child_files_from_drive_id(parent_id=Google_Drive["Evidence"]["id"])

	# Download evidence files
	download_drive_files(file_list=evidence_files, debug=True)

	# Generate p107 documents for events from files
	generate_templates(debug=True)


	print("finished!")