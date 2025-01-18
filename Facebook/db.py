from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Function that initializes the db and creates the tables
def db_init(app):
    db.init_app(app)

    #Creates the database if not already exist
    with app.app_context():
        db.create_all()