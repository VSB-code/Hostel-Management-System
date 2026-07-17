from flask import Flask
from config import Config
from routes import register_blueprints

def create_app():
    """Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    
    # Register all blueprints (routes)
    register_blueprints(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG)