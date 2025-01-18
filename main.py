from flask import Flask, render_template
from YouTube.youtube import youtube_blueprint, delete_record
from YouTube.db import db_init
from Facebook.facebook import facebook
from Facebook.db import db_init as fb_db_init

# init the flask app and the blueprint
app = Flask(__name__)
app.register_blueprint(youtube_blueprint, url_prefix='/facetube/youtube')
app.register_blueprint(facebook, url_prefix='/facetube/facebook')

# configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Videos.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facebook_DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# secret key
app.secret_key = '1234'

# init the database
db_init(app)
fb_db_init(app)

# Home/Main route
@app.route('/')
@app.route('/facetube')
def home():
    return render_template('index.html')


@app.route('/clear')  # Route for cleaning the database after reloading the page -> redirects to /facetube/youtube
def clear():
	delete_record()
	return 'No Need to return anything'

# The main running block
if __name__ == '__main__':
	app.run(host='0.0.0.0')
