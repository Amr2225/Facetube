import os
import subprocess
from pytube import YouTube
from flask import flash, url_for, redirect
from time import sleep
from hurry.filesize import size as transform_size

# Changing the current working directory
os.chdir(os.path.join(os.path.dirname(__file__)))

# Special chracters that must be removed
specialChracters = {
	"?", "|", "*", "!"
}


def get_streams(url) -> str:
	"""
	Getting the url.
	:param url str
		take the url object return from pytube

	:rtype: yt YouTube object
	"""
	try:
		yt = YouTube(url)
		return yt
	except:
		pass


def get_video_info(yt, res=None, fps=None):
	"""
	Gets all the video information
	:param yt YouTube object
		Takes the Youtube object instance
	:param res str
		The wanted resolution ex:'1080p'
	:param fps int
		the wanted fps

	:rtype class:Youtube.streams(video), str(extension), str(video.mime_type), str(name), str(thumbnail_url), str(views), str(date), str(size) 
	"""
	try:
		video = yt.streams.filter(resolution=res, fps=fps, adaptive=True).first()  # Getting the first video that matches the filters
	except AttributeError:
		return False
	name = f'{video.title}.mp4'
	extension = video.default_filename.rsplit('.', 1)[1]  # Gets the extension of the video file
	thumbnail_url = yt.thumbnail_url
	duration = fix_duration(yt.length)
	views = f'{yt.views:,}' # Puts , between digits 1758989 -> 1,758,989
	date = to_date(yt.publish_date)
	size = transform_size(video.filesize)
	return video, extension, video.mime_type, name, duration, thumbnail_url, views, date, size  #video is passed to the convert function only


def get_audio(yt, name):
	audio = yt.streams.get_audio_only()
	size = transform_size(audio.filesize)
	path = os.path.join(os.path.dirname(__file__), 'Audio')
	audio.download(output_path=path, filename='audio')

	# Checks if the name contains special chracters
	name = strip_name(name)
	mp3_filepath = f'{path}/{name.replace("mp4", "mp3")}'

	# The converting to mp3
	cmd = f'ffmpeg -i "{path}/audio.mp4" "{mp3_filepath}"'
	subprocess.run(cmd, shell=True) # running the command
	return path, mp3_filepath, audio.mime_type, size


def convert(yt, video, name, extension):
	"""
	The Merging of video and audio, the main logic.
	:param class:Youtube(yt)
		Takes the Youtube object instance
	:param class:Youtube.streams(video)
		Takes the Youtube.streams object instance returned form the get_video_info function
	:param name str
		The name of the file
	:param extension str
		The extension of the video file

	:rtype: path(directory)
		The absolute path for the combined file
	"""
	os.chdir(os.path.join(os.path.dirname(__file__)))
	audio = yt.streams.get_audio_only()
	video.download(filename='Video')
	audio.download(filename='Audio')

	directory = os.path.join(os.path.dirname(__file__), 'Videos')
	# Checks if the name contains special chracters
	name = strip_name(name)

	cmd = f'ffmpeg -i Video.{extension} -i Audio.mp4 -c copy "{directory}/{name}"'  # ffmpeg code to merge the video and audio
	subprocess.run(cmd, shell=True) # running the command
	sleep(1)
	os.remove(f'Video.{extension}') # removing the video file
	os.remove('Audio.mp4')  # removing the audio file
	return f'{directory}/{name}'


def get_resolutions(yt):
	"""
	Return all the resolutions in orderd state
	:param class: Youtube
		Takes the Youtube object instance

	:rtype list[resolutions]
	"""
	try:  # Checks if there is any problem in the yt object
		list = yt.streams.filter(adaptive=True, type='video')
	except AttributeError:
		print('wrong url')
		return get_streams(yt)
	fpsRes = set()  # initalize a set
	for i in list:
		if i.resolution:  # Geting the resolutions and fps 
			res = str(i.resolution)
			fps = str(i.fps)
			both = str(res + fps)  # Combines the res and fps
			print(both)
			fpsRes.add(both)  # adds the resolution to a list to there will be no duplicates
		resolutions = sorted(fpsRes)  # using sort only to convert the set to a list

	import re

	def atoi(text):
		return int(text) if text.isdigit() else text

	def natural_keys(text):
		'''
		alist.sort(key=natural_keys) sorts in human order
		http://nedbatchelder.com/blog/200712/human_sorting.html
		(See Toothy's implementation in the comments)
		'''
		return [atoi(c) for c in re.split(r'(\d+)', text) ]

	resolutions.sort(key=natural_keys)  # Sorting the resolution and fps
	resolutions.reverse()
	return resolutions


def to_date(date):
	"""
	Just a better formating for the date
	:param date datetime

	:rtype str
	"""
	return date.strftime('%b %d %Y') # Month day Year -> Feb 12 2013  ###%b for the short month name


def fix_duration(duration):
	"""
	Just to fix the duration subtracts 10 from it and removes the . with : and if the length is like this 2:1 it add 0 to the end
	:param duration int

	:rtype duration str
	"""
	length = round((duration / 60), 2)
	if len(str(length)) == 3:
		length = str(length) + '0'
	return str(length).replace('.', ':')


def strip_name(name):
	for char in specialChracters:
		for letter in name:
			if char == letter:
				name = name.replace(char, '')
	# if name[-1] == ' ':
	# 	name = name.rstrip()
	return name
