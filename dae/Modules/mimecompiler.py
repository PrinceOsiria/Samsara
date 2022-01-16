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
def determine_length_of_audio_file(verbose=True, file=None):
	if verbose: print(file)
	return MP3(file).info.length


# Generate Gif File
def generate_gif_file(directory=None, directory_modifier="", files=None, file_name=None, length=None, image_size=(1000,1000), length_delay=0, verbose=True):

	# Initialize the output filename
	output_file_name = directory + directory_modifier + file_name + ".gif"
	if verbose: print(f"Output file name: {output_file_name}\nOutput file Directory: {directory}")

	# Scan directory for requested files
	img, *found_files = [Image.open(directory+file).resize(size=image_size) for file in os.listdir(directory) if file in files]
	if verbose: print(f"Found Files:{found_files}")

	# Modify length input (expected movipy audio length) to work with PIL
	adjusted_length = ((length*1000) + length_delay)/len(files) 
	if verbose: print(f"Length of gif adjusted, saving file")

	# Output the file
	img.save(fp=output_file_name, format='GIF', save_all=True, duration=adjusted_length, loop=0, append_images=found_files)
	if verbose: print(f"File Saved as {file_name}.gif")

	# Return the filename
	return file_name + ".gif"


# Compile Audio Files
def compile_audio_files(files=None, directory=None, file_name=None, file_format="mp3"):
	
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
def create_video(directory=None, audio=None, video=None, gif=None, gif_audio=None, file_name=None, verbose=True, blank_video_directory=None, blank_video=None, blank_png_directory=None, blank_png=None):

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

	# Video File
	if os.path.exists(directory+video):
		video = VideoFileClip(directory + video)
		video.resize( (1000,1000))

	else:
		if verbose: print(f"{directory+video} was not Found")

		# Interferance Patch
		video = VideoFileClip(blank_video_directory + blank_video).subclip(10, 11)

	# Audio File
	if os.path.exists(directory+audio):
		tmp_audio = VideoFileClip(directory + generate_gif_file(directory=blank_png_directory, directory_modifier="tmp/", files=[blank_png], file_name=f"{file_name} - Audio Compilation Gif", length=determine_length_of_audio_file(file=directory+audio), image_size=(1000,1000), length_delay=0))
		tmp_audio.audio = AudioFileClip(directory + audio)
		audio = tmp_audio
	else:
		if verbose: print(f"{directory+audio} was not Found")

		# Interferance Patch
		audio = VideoFileClip(blank_video_directory + blank_video).subclip(10, 11)



	# Combine the Clips
	output = concatenate_videoclips([gif, video, audio])

	# Optional Output
	if verbose: print(f"Writing Video File:\t{directory+file_name}")

	# Export the video file
	output.write_videofile(directory+file_name)
