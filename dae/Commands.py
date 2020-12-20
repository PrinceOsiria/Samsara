###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from dae import *

###########################################################################################################################################
##################################################### Commands ############################################################################
###########################################################################################################################################
# Encode Hels
@dae.command()
async def encode(ctx, clearText, alphaKey, keys):
	# Variable Initialization
	alphabet = p108.create_alphabet(alphaKey)
	clearText = p108.clean_text(clearText, alphabet)
	encodeKeys = p108.clean_text(keys.replace(" ", "~"), alphabet).replace("~", " ")

	# Encryption	
	cipherText = p108.encode_hels(alphabet, encodeKeys.split(), clearText)

	# Output formatting
	embed = discord.Embed()
	embed.add_field(name="__Cleartext__:", value = "*" + clearText + "*", inline = False)
	embed.add_field(name="__Alphabet__:", value = "*" + "".join(alphabet) + "*", inline = False)
	embed.add_field(name="__Keys__:", value = "*" + keys + "*", inline=False)
	embed.add_field(name="__Ciphertext__:", value = "*" + cipherText + "*", inline = False)	

	# Return
	await ctx.send(embed=embed)


# Decode Hels
@dae.command()
async def decode(ctx, cipherText, alphaKey, keys):
	# Variable Initialization
	alphabet = p108.create_alphabet(alphaKey)
	cipherText = p108.clean_text(cipherText, alphabet)
	decodeKeys = p108.clean_text("~".join(reversed(keys.split())), alphabet).replace("~", " ")

	# Decryption	
	clearText = p108.decode_hels(alphabet, decodeKeys.split(), cipherText)

	# Output Formatting
	embed = discord.Embed()
	embed.add_field(name="__Ciphertext__:", value = "*" + cipherText + "*", inline = False)
	embed.add_field(name="__Alphabet__:", value = "*" + "".join(alphabet) + "*", inline = False)
	embed.add_field(name="__Keys__:", value = "*" + keys + "*", inline=False)
	embed.add_field(name="__Cleartext__:", value = "*" + clearText + "*", inline = False)	

	# Return
	await ctx.send(embed=embed)