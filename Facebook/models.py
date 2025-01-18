from Facebook.db import db

class Facebook_DB(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	data = db.Column(db.LargeBinary, unique=True, nullable=False)
	mime_type = db.Column(db.Text, nullable=False)
