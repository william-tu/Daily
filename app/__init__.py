from flask import Flask
from flask_mongoengine import MongoEngine
from elasticsearch import Elasticsearch


from config import config


db = MongoEngine()
client = Elasticsearch()

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)



    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app







