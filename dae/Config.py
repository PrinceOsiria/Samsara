###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# Output options
command_prefix = "!"
selected_output_option = "minimal_med"
root_folder_id = "1QeQJ7diP9_IpOXZ-h_8Xt66psvWyKfBv"


output_options = dict(

	custom = dict(
			cleanup_sequence = True,
			dirty_current_events = False,
			cleaner_actions = True,
			clean_current_events = False,
			event_internalization = False,
			database_update = True,
			new_events = True,
			new_events_plus = True,
			drive_scan = True
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
			drive_scan = True
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
			drive_scan = True
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
			drive_scan = False
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
			drive_scan = True
	)
)