from flask import Flask
from .config import Config
from flask_caching import Cache
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

# Define db here
db = SQLAlchemy()
cache = Cache()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    
    # Initialize the cache
    cache.init_app(app)
    print(f"Cache backend in use: {type(cache.cache).__name__}")

    # Initialize the API
    api.init_app(app)

    #avoid circular import
    from .routes import analytics_bp
    api.register_blueprint(analytics_bp)

    return app
