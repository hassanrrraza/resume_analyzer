import os

class Config:
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-development-only'
    DEBUG = False
    TESTING = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join('app', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Analysis settings
    DEFAULT_WEIGHTS = {
        'required_skills': 0.6,
        'preferred_skills': 0.2,
        'semantic_similarity': 0.2
    }
    
    # Skills database
    SKILLS_DB_PATH = 'skills_db.json'
    
    # PDF report settings
    PDF_OUTPUT_PATH = os.path.join('app', 'uploads', 'results.pdf')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    ENV = 'testing'
    

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    ENV = 'production'
    # SECRET_KEY will be loaded from environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # The check for its existence is now in app/__init__.py


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration based on environment."""
    if not config_name:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    return config.get(config_name, config['default'])() # Instantiate the config class
