# This is the main py file in this app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login= LoginManager(app)
login.login_view = 'login'

#### To be able to drop tables from sqlalchemy
# thanks to render_as_batch function
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

##### Import routes here to avoid circular imports
from stockapp import routes
