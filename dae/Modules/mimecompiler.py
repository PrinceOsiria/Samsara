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
def generate_gif_file(directory=None, files=None, file_name=None, length=None, image_size=(1000,1000), length_delay=0):

	# Initialize the output filename
	output_file_name = directory + file_name + ".gif"
	
	# Scan directory for requested files
	img, *found_files = [Image.open(directory+file).resize(size=image_size) for file in os.listdir(directory) if file in files]
	
	# Modify length input (expected movipy audio length) to work with PIL
	adjusted_length = ((length*1000) + length_delay)/len(files) 
	
	# Output the file
	img.save(fp=output_file_name, format='GIF', save_all=True, duration=adjusted_length, loop=0, append_images=found_files)
	
	# Return the filename
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
	supported_filetypes = ["avi", "mp4"]
	supported_files = []

	# Filter and collect the desired files - NOTE: If forms are configured correctly this becomes redundant
	for file in os.listdir(directory):
		if file in files:
			filetype = file.split(".")[1]

			if filetype in supported_filetypes:
				clip = VideoFileClip(directory+file)
				supported_files.append(clip.resize( (1000,1000) ))
			else: print(filetype)


	# Combine the video clips
	output = concatenate_videoclips(supported_files, method="compose")

	# Export the recombined video file
	output.write_videofile(directory+file_name)
	return file_name


# Create Video
def create_video(directory=None, video=None, gif=None, gif_audio=None, file_name=None, verbose=False, blank_video_directory="C:/Users/tyler/Documents/GitHub/Samsara/dae/Archive/", blank_video="blank.mp4"):

	# Optional Output
	if verbose: print(f"Internalizing gif:\t{directory+gif}")

	# Internalize gif
	gif = VideoFileClip(directory + gif)
	gif.resize( (1000,1000))

	# Optional Output
	if verbose: print(f"Adding Audio to Gif:\t{directory+gif_audio}")

	# Play audio over gif
	gif.audio = AudioFileClip(directory + gif_audio)

	# Optional Output
	if verbose: print(f"Internalizing Video:\t{directory+video}")

	# Internalize the compiled media files - Note: Audio not supported (you try getting it to work)
	if os.path.exists(directory+video):
		video = VideoFileClip(directory + video)
		video.resize( (1000,1000))

	else:
		if verbose: print(f"No Video File was Found")

		# Interferance Patch
		video = VideoFileClip(blank_video_directory + blank_video).subclip(10, 11)


	# Combine the Clips
	output = concatenate_videoclips([gif, video])

	# Optional Output
	if verbose: print(f"Writing Video File:\t{directory+file_name}")

	# Export the video file
	output.write_videofile(directory+file_name)
