from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    from app.scheduling import scheduling_bp
    app.register_blueprint(scheduling_bp)

    from app.negotiation import negotiation_bp
    app.register_blueprint(negotiation_bp)

    from app.purchasing import purchasing_bp
    app.register_blueprint(purchasing_bp)

    from app.shared import shared_bp
    app.register_blueprint(shared_bp)
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app