# App/__init__.py

from flask import Flask
import config

# App creation
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_pyfile('config.py')
    return app
