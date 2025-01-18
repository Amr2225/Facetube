from YouTube.db import db

class Video(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	data = db.Column(db.LargeBinary(4294967295), unique=True, nullable=False)
	thumbnail_url = db.Column(db.String(60), unique=True, nullable=False)
	duration = db.Column(db.String(20), unique=True, nullable=False)
	views = db.Column(db.String(30), nullable=False)
	date = db.Column(db.String(20), nullable=False)
	size = db.Column(db.String(10), nullable=False)
	mime_type = db.Column(db.Text, nullable=False)
