import os
from flask import Flask
from config import get_config, ProductionConfig

def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)

    # Check for SECRET_KEY in production after loading config
    if isinstance(config_obj, ProductionConfig) and not app.config.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY must be set in the environment for production.")
    
    # Ensure the upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app