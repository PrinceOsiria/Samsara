###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Imports
from samsara import *

# Discord Archiving Engine Module
from samsara.Modules.dae_functions import *

# Nameless Index Timeline Engine Module
from samsara.Modules.nite_functions import *

###########################################################################################################################################
##################################################### Tasks $##############################################################################
###########################################################################################################################################
# Task Practice
@tasks.loop(seconds=120)
async def karma():

	# Non-Optional Output
	if output: print(f"""
###########################################################################################################################################
Codename Samsara is: ONLINE""")


	##### CONFIRMED WORKING AREA
	initiate_automated_cleanup()
	update_database(get_current_events())


	##### EXPERIMENTAL AREA
	validate_database()


	# Non-Optional Output
	if output: print(f"""
Codename Samsara is: OFFLINE
###########################################################################################################################################""")