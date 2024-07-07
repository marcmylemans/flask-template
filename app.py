from flask import Flask, render_template, session, redirect, url_for, request, flash, request, Response
from flask_migrate import Migrate
from models import db, User
from auth import auth as auth_blueprint
from dotenv import load_dotenv
from datetime import datetime
import os
import pathlib
import pyotp



load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

def create_database(app):
    """Create the SQLite database file if it doesn't exist."""
    database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if database_uri.startswith("sqlite:///"):
        db_file = pathlib.Path(database_uri.partition(":///")[2])
        if not db_file.is_file():
            with app.app_context():
                db.create_all()
            print("Created SQLite database.")

create_database(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success')
def success():
    instance_info = session.get('instance_info')
    return render_template('success.html', instance_info=instance_info)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy-policy')
def privacy_policy():
    current_year = datetime.now().year
    return render_template('privacy_policy.html', current_year=current_year)

# ... other routes ...




if __name__ == '__main__':
    app.run(debug=True)
