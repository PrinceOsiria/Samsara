###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# Google Text-To-Speech
import gtts
from playsound import playsound
from mutagen.mp3 import MP3
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
#Working Directory
working_directory = "C:/Users/tyler/Documents/GitHub/Samsara/dae/Archive/tmp/"


###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Convert Text to Audio File
def convert_text_to_audio_file(text=None, directory=None, file_name=None):
	gtts.gTTS(text).save(directory+file_name+".mp3")
	return (directory+file_name+".mp3")

# Determine Length of audio file
def determine_length_of_audio_file(file=None):
	return MP3(file).info.length


# Generate Gif File
def generate_gif_file(directory=None, files=None, file_name=None, length=None, length_delay=0):
	output_file_name = directory + file_name + ".gif"
	img, *found_files = [Image.open(directory+file) for file in os.listdir(directory) if file in files]
	adjusted_length = ((length*1000) + length_delay)/len(files) 
	img.save(fp=output_file_name, format='GIF', save_all=True, duration=adjusted_length, loop=0, append_images=found_files)
	return output_file_name


# Compile Audio Files
def compile_audio_files(files=None, directory=None, file_name=None, file_format="mp3"):
	
	supported_filetypes = ["mp4", "mp3", "flv", "ogg", "wma", "aac", "wav", "mpeg", ]
	supported_files = []

	# Filter and collect the desired files - NOTE: If forms are configured correctly this becomes redundant
	for file in os.listdir(directory):
		if file in files:
			filetype = file.split(".")[1]

			if filetype in supported_filetypes:
				supported_files.append(AudioSegment.from_file(directory+file, filetype))

	# Combine the supported audio segments
	output = AudioSegment.empty()
	for file in supported_files:
			output += file

	# Export the recombined audio file
	output.export(directory+file_name, format=file_format)
	return directory+file_name


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
	return directory+file_name

###########################################################################################################################################
##################################################### Main ################################################################################
###########################################################################################################################################
# Convert text to audio
#audio_file_directory = convert_text_to_audio_file(text="This is a very monumentous moment, as we have now established all we need to move foreward.", directory=working_directory, file_name="test")

# Determine length of audio
#length = determine_length_of_audio_file(file=audio_file_directory)

# Generate Gif File
#gif_file = generate_gif_file(directory=working_directory, files=["ferns.jpg", "ferns2.jpg"], file_name="testpassed", length=length, length_delay=3000)

# Compile Audio Files
#compile_audio_files(files=["test.mp3", "test2.mp3"], directory=working_directory, file_name="testpassed.mp3")


# Compile Video Files
#compile_video_files(files=["test.mp4", "test2.mp4"], directory=working_directory, file_name="testpassed.mp4")

