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
@tasks.loop(hours=1)
async def samsara():

	# Non-Optional Output
	if output: print(f"""
###########################################################################################################################################
Codename Samsara is: ONLINE
""")


	# Debug Halt
	if debug_halt: print("Please Press Enter to Begin"); input()

	# Initialization and Validation - N.I.T.E.
	initiate_automated_cleanup()

	# Debug Skip
	if not debug_skip:
		scan_drive()
		validate_cloud_integrity()

		# D.A.E.
		update_database(get_current_events())
		
		# N.I.T.E.
		archive_events(identify_new_events())
		generate_timeline_videos(identify_new_videos()) # Unindented to debug
		

	# Non-Optional Output
	if output: print(f"""
Codename Samsara is: OFFLINE
###########################################################################################################################################""")
