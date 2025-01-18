from flask import Blueprint, redirect, url_for, render_template, request, flash, Response, jsonify, abort
from Facebook.Logic import download_video, get_filename, convert
from Facebook.models import Facebook_DB
from Facebook.db import db
from time import sleep
import werkzeug
import os

facebook = Blueprint('facebook', __name__, static_folder='static', template_folder='templates')


@facebook.route('/')
def home():
    return render_template('facebook_home.html')


@facebook.route('/download', methods=['POST'])
def download():
    delete_record()

    url = request.form['URL']
    directory = download_video(url)

    if type(directory) is werkzeug.wrappers.response.Response:
        return redirect(url_for('facebook.home'))
    
    if not directory:
        directory = os.path.join(os.path.dirname(__file__), 'Videos')

    filename = get_filename(directory)
    location = os.path.join(directory, filename)

    facebook_db = Facebook_DB(name=filename, data=open(location, 'rb').read(), mime_type='video/mp4')
    db.session.add(facebook_db)
    db.session.commit()

    os.remove(location)
    sleep(1.5)
    return redirect(url_for('facebook.home'))


@facebook.route('/send')
def send():
    video = Facebook_DB.query.filter_by(id=1).first()
    if not video:
        abort(404)
    return Response(video.data, mimetype=video.mime_type)


@facebook.route('/get')
def get():
    video = Facebook_DB.query.filter_by(id=1).first()
    if not video:
        abort(404)
    return jsonify(name=video.name, id=video.id, url=url_for('facebook.send'))


@facebook.route('/get_audio')
def getAudio():
    return render_template('audio.html')


@facebook.route('/download_audio', methods=['POST'])
def downloadAudio():
    delete_record()

    url = request.form['URL']
    directory = download_video(url)

    if type(directory) is werkzeug.wrappers.response.Response:
            return redirect(url_for('facebook.getAudio'))
    
    if not directory:
        directory = os.path.join(os.path.dirname(__file__), 'Videos')

    filenmae = get_filename(directory)
    print('the type', filenmae, directory)
    output_path = convert(directory, filenmae)

    facebook_db = Facebook_DB(name=filenmae.replace('mp4', 'mp3'), data=open(output_path, 'rb').read(), mime_type='audio/mp3')
    db.session.add(facebook_db)
    db.session.commit()

    os.remove(output_path)
    sleep(1.5)
    return redirect(url_for('facebook.getAudio'))


def delete_record():  # Simple function used to delete any acess records
	records = db.engine.execute('SELECT id FROM facebook_DB ORDER BY id ASC LIMIT 1')
	id = 0
	for record in records:
		id = record
	try:
		# print('this is the id ', id[0])
		deletion = Facebook_DB.query.filter_by(id=id[0]).first()
		db.session.delete(deletion)
		db.session.commit()
	except:
		print('no data')  
