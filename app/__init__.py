from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flasgger import Swagger
from flask_cors import CORS
import logging

db = SQLAlchemy()
swagger = Swagger()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_prefix = '/api'
    
    db.init_app(app)
    swagger.init_app(app)
    cors.init_app(app)

    # log to console
    logging.basicConfig(level=logging.DEBUG)

    # Registering Blueprints
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