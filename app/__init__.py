from flask import Flask
from .config import Config
from flask_caching import Cache
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .routes import analytics_bp

db= SQLAlchemy()
cache = Cache()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    
    # Initialize the cache
    cache.init_app(app)

    # Initialize the API
    api.init_app(app)
    api.register_blueprint(analytics_bp)

    return app
