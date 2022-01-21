###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Core Discord Imports
from dae import *

###########################################################################################################################################
##################################################### Commands ############################################################################
###########################################################################################################################################

# Help
@dae.command()
async def help(ctx):
	# Output formatting
	embed = discord.Embed()
	embed.add_field(name="__Project Samsara__", value ="Welcome to Project Samsara! For help with my commands, please visit this link:", inline = False)
	embed.add_field(name="__Documentation__", value ="https://tinyurl.com/samsaradocumentation", inline = False)

	# Return
	await ctx.send(embed=embed)

# Home
@dae.command()
async def home(ctx):
	# Output formatting
	embed = discord.Embed()
	embed.add_field(name="__Project Samsara__", value =f"Welcome Back {ctx.message.author.mention}", inline = False)
	embed.add_field(name="__Project 107__", value ="https://tinyurl.com/samsarahome", inline = False)

	# Return
	await ctx.send(embed=embed)

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


# Request Information on a particular timeframe
@dae.command()
async def index(ctx, timeframe="0000", event_title=None):

	# Parse User Input
	if timeframe:

		# Allow for !index usage on it's own
		year_override=False
		if timeframe == "0000": 
			timeframe_length = 0
		else:
			timeframe = timeframe.split("/")
			timeframe_length = len(timeframe)


		# Format the Input
		year, month, day = None, None, None
		year_exists, month_exists, day_exists = None, None, None
	

		# Query Database
		if timeframe_length > 0: 
			year = timeframe[0]
			year_exists = session.query(Year).filter_by(year=year).first()
	

		if timeframe_length > 1: 
			month = timeframe[1]
			month_exists = session.query(Month).filter_by(month=month).first()
	

		if timeframe_length > 2: 
			day = timeframe[2]
			day_exists = session.query(Day).filter_by(day=day).first()


		# Allow listing found events
		if event_title:
			event_exists = session.query(Event).filter_by(title=event_title).first()
		else:
			event_exists = False


		# Prepare the Output
		embed = discord.Embed()
		

		# Determine the correct data to output
		if year_exists: 
			if month_exists:
				if day_exists:
					if event_exists:
						requested_id = event_exists.event_video_summary_file
						event_summary_document = event_exists.event_summary_file
						event_tags = event_exists.tags

					# day
					else:
						requested_id = day_exists.document_id
						requested_video_id = month_exists.video_id
						found_data = session.query(Event).filter_by(day=day_exists).all()
						data_type = "event"

						export = []
						for found_event in found_data:
							export.append(found_event.title)

						found_data = export

				# Month
				else:
					requested_id = month_exists.document_id
					requested_video_id = month_exists.video_id
					found_data = session.query(Day).filter_by(month=month_exists).all()
					data_type = "day"

					export = []
					for found_day in found_data:
						export.append(str(found_day.day))

					found_data = export

			# Year
			else:
				requested_id = year_exists.document_id
				requested_video_id = year_exists.video_id
				found_data = session.query(Month).filter_by(year=year_exists).all()
				data_type = "month"

				export = []
				for found_month in found_data:
					export.append(str(found_month.month))

				found_data = export
		
		# None
		else:
			requested_id = False
			found_data = session.query(Year).all()
			data_type = "year"

			export = []
			for found_year in found_data:
				export.append(str(found_year.year))

			found_data = export


		# Determine which output to use
		# Event Data Found
		if event_exists:
			embed.add_field(
				name=f"*__Index__*",
				value=f"""
				{ctx.message.author.mention} has requested:
					\tYear: {year}
					\tMonth: {month}
					\tDay: {day}
					\tEvent: {event_title}
					\tTags: {event_tags}

				\nEvent Document:
				https://docs.google.com/document/d/{event_summary_document}

				\nSummary Video:
				https://drive.google.com/file/d/{requested_id}
			""")


		# Timeframe Data Found
		elif requested_id:
			embed.add_field(
				name=f"*__Index__*",
				value=f"""
				{ctx.message.author.mention} has requested: 
					\tYear: {year}
					\tMonth: {month}
					\tDay: {day}

				\n Here are the {data_type}s I found:
				{found_data}

				\nTimeline Document
				https://docs.google.com/document/d/{requested_id}

				\n Timeline Video
				https://drive.google.com/file/d/{requested_video_id}/view?usp=sharing
			""")


		# No Data Found
		else:
			if year:
				message = f"There are no events archived under the year {year}"
			else:
				message = ""

			embed.add_field(
				name=f"*__Index__*",
				value=f"""
				{message}

				\n Here are the years I found:
				{found_data}
			""")
		

		# Return
		await ctx.send(embed=embed)


# Return Current Events
@dae.command()
async def current_events(ctx):
	# Get all Years
	years = session.query(Year).all()

	# Get Current Year
	max_year = 0
	for year in years:
		if int(year.year) > int(max_year):
			current_year = year
			max_year = year.year

	# Get Current Month
	max_month = 0
	for month in current_year.months:
		if int(month.month) > max_month:
			current_month = month
			max_month = month.month

	# Gather the required resources
	requested_id = month.document_id
	requested_video_id = month.video_id
	days = []
	for day in month.days:
		days.append(day.day)

	# Prepare the output
	embed = discord.Embed()
	embed.add_field(
		name=f"*__Current Events__*",
		value=f"""
		{ctx.message.author.mention} has requested: 
			\tYear: {year.year}
			\tMonth: {month.month}

		\n Here are the days I found:
		{days}

		\nTimeline Document
		https://docs.google.com/document/d/{requested_id}

		\n Timeline Video
		https://drive.google.com/file/d/{requested_video_id}/view?usp=sharing
	""")

	# Return
	await ctx.send(embed=embed)

# Catch the user up
@dae.command()
async def catchmeup(ctx, timeframe=None):

	# Prepare the Output
	embed = discord.Embed()	

	if timeframe:

		# Format the Input
		timeframe = timeframe.split("/")
		timeframe_length = len(timeframe)
		year, month = None, None
		year_exists, month_exists = None, None
		if timeframe_length > 0: year = int(timeframe[0])
		if timeframe_length > 1: month = int(timeframe[1])

		# Get Current Year
		requested_year = session.query(Year).filter_by(year=year).first()
		if requested_year:
			if year == requested_year.year: 
				year_exists = True
				current_year = requested_year

		# Get Current Month
		if month:
			requested_month = session.query(Month).filter_by(month=month).first()
			if month == requested_month.month: 
				month_exists = True
				current_month = requested_month

		# Input Validation
		if year_exists:
			if month_exists:
				# Fetch remaining months of current year
				requested_months = []
				max_month = int(current_month.month)
				for month in current_year.months:
					if int(month.month) > max_month:
						requested_months.append(month)


			# Fetch the requested future years
			requested_years = []
			years = session.query(Year).all()
			for tmp_year in years:
				if tmp_year.year > year:
					requested_years.append(tmp_year)


			# Prepare the Output	
			if month_exists:
				embed.add_field(name=f"*__Catch Me Up__*",value=f"""{ctx.message.author.mention} has requested all new entries after (and including) {current_year.year}/{current_month.month}:""")
				embed.add_field(name=f"*__{current_year.year}/{current_month.month}__*",value=f"""
							\nTimeline Document
							https://docs.google.com/document/d/{current_month.document_id}

							\n Timeline Video
							https://drive.google.com/file/d/{current_month.video_id}/view?usp=sharing
					""")
				
				for month in requested_months:
					embed.add_field(name=f"*__{month.year.year}/{month.month}__*",value=f"""
							\nTimeline Document
							https://docs.google.com/document/d/{month.document_id}

							\n Timeline Video
							https://drive.google.com/file/d/{month.video_id}/view?usp=sharing
					""")

			else:
				embed.add_field(name=f"*__Catch Me Up__*",value=f"""{ctx.message.author.mention} has requested all new entries after (and including) {current_year.year}:""")
				embed.add_field(name=f"*__{current_year.year}__*",value=f"""
							\nTimeline Document
							https://docs.google.com/document/d/{current_year.document_id}

							\n Timeline Video
							https://drive.google.com/file/d/{current_year.video_id}/view?usp=sharing
					""")	


			for year in requested_years:
				embed.add_field(name=f"*__{year.year}__*",value=f"""
						\nTimeline Document
						https://docs.google.com/document/d/{year.document_id}

						\n Timeline Video
						https://drive.google.com/file/d/{year.video_id}/view?usp=sharing
				""")

			
		else:
			embed.add_field(name=f"*__Catch Me Up__*",value=f"""
						I could not find that year in my database
						Please use `!index` to explore the archives and try again with a valid timeframe
						""")
	else:
		embed.add_field(name=f"*__Catch Me Up__*",value=f"""
						Please use `!index` to explore the archives and try again with a valid timeframe
						""")
	# Return
	await ctx.send(embed=embed)


# Filter events by tag
@dae.command()
async def filter(ctx, tags=None):

	# Allows for use without tags
	if not tags:
		requested_events = None

		# Collect all known tags
		tags = []
		for event in session.query(Event).all():
			for tag in event.tags.replace(" ", "").split(","):
				if tag not in tags:
					tags.append(tag)

	else:


		tags = tags.split(",")
		events = session.query(Event).all()

		requested_events = []
		for event in events:

			# Initialize the filter (return only if all tags are found)
			number_of_tags = len(tags)
			number_of_matches = 0

			# Scan the event for matched tags
			for tag in tags:
				if tag in event.tags:
					number_of_matches += 1

			# Output the event if it contains the requested tags
			if number_of_matches == number_of_tags:
				requested_events.append(event)


	# Prepare Output
	embed = discord.Embed()
	if requested_events:
		for event in requested_events:
			embed.add_field(name=f"__{event.title}__", value=f"""
			\nTags: {event.tags}


			\nTimeline Document
			https://docs.google.com/document/d/{event.event_summary_file}

			\n Timeline Video
			https://drive.google.com/file/d/{event.event_video_summary_file}/view?usp=sharing

				""")
	else:
		embed.add_field(name=f"__Filter__", value=f"""
			\n To use filter, you must supply tags! Here are the tags I found:


			\n{tags}
				""")
			
			

	# Return
	await ctx.send(embed=embed)
