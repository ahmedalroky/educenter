from flask import Flask
from .api.user_routes import user_bp
from .api.school_routes import school_bp
# Import other blueprints...

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(school_bp)
    # Register other blueprints...
    return app
