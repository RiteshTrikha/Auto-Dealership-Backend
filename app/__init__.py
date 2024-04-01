from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    from app.api import api
    api.init_app(app)

    # Configure logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Registering Blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp)

    from app.customer import customer_bp
    app.register_blueprint(customer_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    from app.scheduling import scheduling_bp
    app.register_blueprint(scheduling_bp)

    from app.negotiation import negotiation_bp
    app.register_blueprint(negotiation_bp)

    from app.purchasing import purchasing_bp
    app.register_blueprint(purchasing_bp)
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.inventory import inventory_bp
    app.register_blueprint(inventory_bp)

    # Registering Services
    from app.negotiation.services import NegotiationService
    app.negotiation_service = NegotiationService()

    from app.inventory.services import InventoryService
    app.inventory_service = InventoryService()

    @app.before_request
    def before_request():
        g.negotiation_service = current_app.negotiation_service
        g.inventory_service = current_app.inventory_service

    return app