from flask import Flask
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login = LoginManager(app)
login.login_view = 'login'

from app import routes
