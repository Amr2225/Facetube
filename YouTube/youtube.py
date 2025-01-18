from flask import Flask, request, url_for, render_template, session, jsonify, Response, flash, redirect, Blueprint, current_app
from flask_marshmallow import Marshmallow
from pytube import YouTube
from YouTube.db import db
from YouTube.models import Video
from YouTube.Logic import get_video_info, convert, get_streams, get_resolutions, get_audio
from time import sleep
import os

#init the Blueprint
youtube_blueprint = Blueprint('youtube_blueprint', __name__, static_folder='Youtube static', template_folder='Youtube templates')
# init marshmallow
marsh = Marshmallow(youtube_blueprint)

# Making the schema
class VideoSchema(marsh.SQLAlchemySchema):
	class Meta:
		model = Video

	id = marsh.auto_field()
	name = marsh.auto_field()
	views = marsh.auto_field()
	date = marsh.auto_field()
	size = marsh.auto_field()
	duration = marsh.auto_field()
	thumbnail_url = marsh.auto_field()


@youtube_blueprint.route('/')  # The main home page
def home():
	return render_template('home.html')


@youtube_blueprint.route('/home/get', methods=['POST']) # method -> post
def download():
	url = request.form['URL']

	yt = get_streams(url)
	resolutions = get_resolutions(yt)
	try:
		highest_resolution = resolutions.pop(0)
	except:
		flash('Please Enter a valid URL', 'active')
		return redirect(url_for('youtube_blueprint.home'))

	splitted = highest_resolution.rsplit('p', 1) # splites the res and fps
	res, fps = splitted[0]+'p', int(splitted[1])

	video, extension, mime_type, name, duration, thumbnail_url, views, date, size = get_video_info(yt, res, fps)
	directroy = convert(yt, video, name, extension)

	video = Video(name=name, data=open(directroy, 'rb').read(), thumbnail_url=thumbnail_url, duration=duration, views=views, date=date, size=size, mime_type=mime_type)
	os.remove(directroy) # removing the file after uploading to the database
	db.session.add(video)
	try:
		db.session.commit()
	except:
		flash('Unspported file Type Please use a lower resolution in (advanced section)', 'active')
		return redirect(url_for('youtube_blueprint.advance'))
	return redirect(url_for('youtube_blueprint.home'))


@youtube_blueprint.route('/videos')  # The api responsable for the video box
def video():
	videos_schema = VideoSchema(many=True) # init the schema
	record = db.engine.execute('SELECT * FROM video ORDER BY id DESC LIMIT 1') # Getting the oldest video in the database (it is a flaw with the design there always will be one record in the database)
	data = videos_schema.dump(record)  # Dumps the data to the schema to return it in json format

	return jsonify(data) # Formating the data to json


@youtube_blueprint.route('/videos/<int:id>')  # Route for downloading the video
def view(id):
	video = Video.query.filter_by(id=id).first()  # Qurey the video with the specifed id
	return Response(video.data, mimetype=video.mime_type) # Returns the video

#get_audio route
@youtube_blueprint.route('/get_audio')
def getAudio():
	return render_template('get_audio.html')

# Route for posting the audio url and downloading the file
@youtube_blueprint.route('/get_audio/search', methods=['POST'])
def audioSearch():
	delete_record()
	url = request.form['URL']

	yt= get_streams(url)

	try:
		_, _, _, name, duration, thumbnail_url, views, date, _ = get_video_info(yt)
	except TypeError:
		flash('Please Enter a Vaild URL', 'active')
		return redirect(url_for('youtube_blueprint.getAudio'))

	path, mp3_filepath, mime_type, size = get_audio(yt, name)
	audio = Video(name=name.replace("mp4", "mp3"), data=open(mp3_filepath, 'rb').read(), thumbnail_url=thumbnail_url, duration=duration, views=views, date=date, size=size, mime_type=mime_type)
	db.session.add(audio)
	db.session.commit()
	
	filepath = os.path.join(path, 'audio.mp4')
	os.remove(filepath)	
	os.remove(mp3_filepath)	
	return redirect(url_for('youtube_blueprint.getAudio'))

#Route for the advance
@youtube_blueprint.route('/advance', methods=['GET', 'POST'])
def advance():
	flash('hidden', 'class')  # Hiddes the select tag
	# if the resolution is undefined then it will == []
	try:  
		resolutions = session['resolutions']
	except KeyError:
		resolutions = []

	return render_template('advance.html', resolutions=resolutions)


@youtube_blueprint.route('/advance/search', methods=['POST'])  # Route for posting the url -> redirects to /youtubek
def search():
	print('in search funciton')
	delete_record()
	url = request.form['URL'] # Gets the url

	session['url'] = url

	yt = get_streams(url)

	resolutions = get_resolutions(yt) # Gets the order resolutions
	if not resolutions: # if theres no reslutions it means that the url is invalid
		flash('please Enter a valid URL', 'active')
		return redirect(url_for('youtube_blueprint.advance'))

	if 'resolutions' in session: 
		session.pop('resolutions', None)
			
	session['resolutions'] = resolutions # addst the resolutions to the session so we can acess it from /youtube

	flash('visible', 'class') # shows the select tag
	return redirect(url_for('youtube_blueprint.advance'))


@youtube_blueprint.route('/advance/get', methods=['POST']) # Route for posting the resolutions and fps -> redirects to /youtube
def get():
	getting_res = request.form.get('res') # Gets the res and fps
	splitted = getting_res.rsplit('p', 1) # splites the res and fps
	try: # if there is now res then flash an error
		res, fps = splitted[0]+'p', int(splitted[1])
	except IndexError:
		flash('Please Enter the resolution', 'active')
		return redirect(url_for('youtube_blueprint.advance'))

	if 'url' in session:
		url = session['url']

	yt = get_streams(url)

	video, extension, mime_type, name, duration, thumbnail_url, views, date, size = get_video_info(yt, res, fps)

	directroy = convert(yt, video, name, extension)

	session.pop('url', None)  # To remove the url from the session
	
	# Uploading to the database
	# Uploading the file as a blob
	video = Video(name=name, data=open(directroy, 'rb').read(), thumbnail_url=thumbnail_url, duration=duration, views=views, date=date, size=size, mime_type=mime_type)
	os.remove(directroy) # removing the file after uploading to the database
	db.session.add(video)
	try:
		db.session.commit()
	except:
		flash('Unspported file Type Please use a lower resolution in (advanced section)', 'active')
		redirect(url_for('youtube_blueprint.advance'))

	sleep(2)
	return redirect(url_for('youtube_blueprint.advance'))


def delete_record():  # Simple function used to delete any acess records
	records = db.engine.execute('SELECT id FROM video ORDER BY id ASC LIMIT 1')
	id = 0
	for record in records:
		id = record
	try:
		# print('this is the id ', id[0])
		deletion = Video.query.filter_by(id=id[0]).first()
		db.session.delete(deletion)
		db.session.commit()
	except:
		print('no data')  