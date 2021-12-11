###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Input Options
command_prefix = "!"

# Output options
selected_output_option = "custom"

# Drive Filesystem Configuration
root_folder_id = "1QeQJ7diP9_IpOXZ-h_8Xt66psvWyKfBv"

# Local Filesystem Configuration
private_key_location = "C:/Users/tyler/Documents/GitHub/Samsara/dae/Archive" + "/" + "private_key.json"
bot_workspace_location = "C:/Users/tyler/Documents/GitHub/Samsara/dae/Archive/tmp"


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
			cloud_integrity_check = True
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
			cloud_integrity_check = True
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
			cloud_integrity_check = True
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
			cloud_integrity_check = False
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
			cloud_integrity_check = True
	)
)