from elasticsearch import Elasticsearch
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_cors import CORS

from config import config

mail = Mail()
db = MongoEngine()
client = Elasticsearch()
cors = CORS()

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app







