###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from dae import *

###########################################################################################################################################
##################################################### Events ##############################################################################
###########################################################################################################################################
# Bot Initialization
@dae.event
async def on_ready():
	samsara.start()
