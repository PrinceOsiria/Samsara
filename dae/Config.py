###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Operating System Functions
import os

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Drive Filesystem Configuration
root_folder_id = ""
years_document_id = ""

# Local Filesystem Configuration
private_key_location = ""
bot_workspace_location = ""
local_archive_folder_location=""

# Bot Options
command_prefix = "!"

## Debugging Options
## MANUAL
# Prevent the bot from looping on an error
debug_halt = None
# Skip portions of code
debug_skip = None

## AUTOMATIC
# Rebuild the cloud if the local filesystem is missing (results in errors if cloud is occupied)
smart_debug_skip = False
# Turns debug options off
production_mode = True


# Reconfigure Configs
if production_mode:
	debug_halt = False
	debug_skip = False
	smart_debug_skip=False

if smart_debug_skip:
	if "archive.db" not in os.listdir(bot_workspace_location[:-4]): 
		debug_skip = False
		debug_halt = True
	else:
		debug_skip = True
		debug_halt = False


# Output options
selected_output_option = "custom"


# Output Configurations
output_options = dict(

	custom = dict(
			cleanup_sequence = True,
			dirty_current_events = False,
			cleaner_actions = False,
			clean_current_events = False,
			event_internalization = True,
			database_update = True,
			new_events = True,
			new_events_plus = True,
			new_events_more = False,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = True,
			identify_new_videos_more = False,
			generate_new_videos = True,
			generate_new_videos_more = False
	),

	minimal_med = dict(
			cleanup_sequence = True,
			dirty_current_events = False,
			cleaner_actions = True,
			clean_current_events = False,
			event_internalization = False,
			database_update = True,
			new_events = True,
			new_events_plus = False,
			new_events_more = False,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = False,
			identify_new_videos_more = False,
			generate_new_videos = True,
			generate_new_videos_more = False
	),

	minimal_max = dict(
			cleanup_sequence = True,
			dirty_current_events = False,
			cleaner_actions = True,
			clean_current_events = False,
			event_internalization = False,
			database_update = True,
			new_events = True,
			new_events_plus = True,
			new_events_more = False,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = True,
			identify_new_videos_more = False,
			generate_new_videos = True,
			generate_new_videos_more = True
	),

	all_false = dict(
			cleanup_sequence = False,
			dirty_current_events = False,
			cleaner_actions = False,
			clean_current_events = False,
			event_internalization = False,
			database_update = False,
			new_events = False,
			new_events_plus = False,
			new_events_more = True,
			drive_scan = False,
			cloud_integrity_check = False,
			identify_new_videos = False,
			identify_new_videos_more = False,
			generate_new_videos = False,
			generate_new_videos_more = False
	),

	all_true = dict(
			cleanup_sequence = True,
			dirty_current_events = True,
			cleaner_actions = True,
			clean_current_events = True,
			event_internalization = True,
			database_update = True,
			new_events = True,
			new_events_plus = True,
			new_events_more = True,
			drive_scan = True,
			cloud_integrity_check = True,
			identify_new_videos = True,
			identify_new_videos_more = True,
			generate_new_videos = True,
			generate_new_videos_more = True
	)
)