###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Bot Imports
from dae import *

# DAE Functions
from dae.Modules.dae_functions import *

# NITE Functions
from dae.Modules.nite_functions import *

###########################################################################################################################################
##################################################### Tasks ###############################################################################
###########################################################################################################################################
# Task Practice
@tasks.loop(hours=12)
async def samsara():

	# Non-Optional Output
	if output: print(f"""
###########################################################################################################################################
Codename Samsara is: ONLINE
""")


	# Debug Halt
	if debug_halt: print("Please Press Enter to Begin"); input()

	# Automated Cleanup - N.I.T.E.
	initiate_automated_cleanup()

	# Debug Skip - unindent the part you wish to resume from
	if not debug_skip:
		# Initialization and Validation - N.I.T.E.
		if not production_mode:
			scan_drive()
			validate_cloud_integrity()

		# D.A.E.
		update_database(get_current_events())
		
		# N.I.T.E.
		new_events = identify_new_events()
		if new_events:
			archive_events(new_events)
			generate_timeline_videos(identify_new_videos())
			initiate_automated_cleanup()

	# Non-Optional Output
	if output: print(f"""
Codename Samsara is: OFFLINE
###########################################################################################################################################""")
