# medicoblog/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'



#####################################
###### SETUP DO BANCO DE DADOS ######
#####################################


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


##############################
# LOGIN CONFIGS

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from projeto_clinica.core.views import core
from projeto_clinica.usuarios.views import usuarios
from projeto_clinica.error_pages.handlers import error_pages
from projeto_clinica.graficos.graph import graficos_bp
#############################

app.register_blueprint(core)
app.register_blueprint(usuarios)
app.register_blueprint(error_pages)
app.register_blueprint(graficos_bp)