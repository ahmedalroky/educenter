from flask import Flask
from .config.settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Import and register Blueprints
    # Example: from .api.user_routes import user_bp
    # app.register_blueprint(user_bp)
    
    return app
