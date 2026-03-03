from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate, jwt, cors
from .routes import api_bp
from .auth import auth_bp
from . import models
from .requests import requests_bp

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})  # dev only

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(requests_bp)

    return app