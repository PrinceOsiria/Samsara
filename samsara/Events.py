###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from samsara import *

###########################################################################################################################################
##################################################### Events ##############################################################################
###########################################################################################################################################
# Bot Initialization
@Samsara.event
async def on_ready():
	karma.start()
