###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Google Text-To-Speech
import gtts
from playsound import playsound
from mutagen.mp3 import MP3
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import *
import os

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Convert Text to Audio File
def convert_text_to_audio_file(text=None, directory=None, file_name=None):
	gtts.gTTS(text).save(directory+file_name+".mp3")
	return (file_name+".mp3")

# Determine Length of audio file
def determine_length_of_audio_file(file=None):
	return MP3(file).info.length


# Generate Gif File
def generate_gif_file(directory=None, files=None, file_name=None, length=None, length_delay=0):
	output_file_name = directory + file_name + ".gif"
	img, *found_files = [Image.open(directory+file) for file in os.listdir(directory) if file in files]
	adjusted_length = ((length*1000) + length_delay)/len(files) 
	img.save(fp=output_file_name, format='GIF', save_all=True, duration=adjusted_length, loop=0, append_images=found_files)
	return file_name + ".gif"


# Compile Audio Files
def compile_audio_files(files=None, directory=None, file_name=None, file_format="wav"):
	
	supported_filetypes = ["mp4", "mp3", "flv", "ogg", "wma", "aac", "wav", "mpeg", ]
	supported_files = []

	# Filter and collect the desired files - NOTE: If forms are configured correctly this becomes redundant
	for file in os.listdir(directory):
		if file in files:
			filetype = file.split(".")[1]

			if filetype == "x-wav":
				filetype = "wav"

			if filetype in supported_filetypes:
				supported_files.append(AudioSegment.from_file(directory+file, filetype))

	# Combine the supported audio segments
	output = AudioSegment.empty()
	for file in supported_files:
			output += file

	# Export the recombined audio file
	output.export(directory+file_name, format=file_format)
	return file_name


# Compile Video Files
def compile_video_files(files=None, directory=None, file_name=None):
	supported_filetypes = ["mp4", "avi", "flac"]
	supported_files = []

	# Filter and collect the desired files - NOTE: If forms are configured correctly this becomes redundant
	for file in os.listdir(directory):
		if file in files:
			filetype = file.split(".")[1]

			if filetype in supported_filetypes:
				supported_files.append(VideoFileClip(directory+file))


	# Combine the video clips
	output = concatenate_videoclips(supported_files)

	# Export the recombined video file
	output.write_videofile(directory+file_name)
	return file_name


# Create Video
def create_video(directory=None, video=None, gif=None, gif_audio=None, file_name=None, verbose=True):

	# Optional Output
	if verbose == True: print(f"Internalizing gif:\t{directory+gif}")

	# Internalize gif
	gif = VideoFileClip(directory + gif)

	# Optional Output
	if verbose == True: print(f"Adding Audio to Gif:\t{directory+gif_audio}")

	# Play audio over gif
	gif.audio = AudioFileClip(directory + gif_audio)

	# Optional Output
	if verbose == True: print(f"Internalizing Video:\t{directory+video}")

	# Internalize the compiled media files - Note: Audio not supported (you try getting it to work)
	if os.path.exists(directory+video):
		video = VideoFileClip(directory + video)

		# Combine the clips
		output = concatenate_videoclips([gif, video])

	else:
		if verbose: print(f"No Video File was Found")

		# Prepare the Gif for Output
		output = gif

	# Optional Output
	if verbose == True: print(f"Writing Video File:\t{directory+file_name}")

	# Export the video file
	output.write_videofile(directory+file_name)

	# Optional Output
	if verbose == True: print("Nothing is returned")

