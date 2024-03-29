from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flasgger import Swagger
from flask_cors import CORS
from app.error_handlers import register_error_handlers
from flask_jwt_extended import JWTManager
import logging


db = SQLAlchemy()
swagger = Swagger()
cors = CORS()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    swagger.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    

    # Registering Error Handlers
    register_error_handlers(app)

    # log to console
    logging.basicConfig(level=logging.DEBUG)

    # Registering Blueprints

    api_prefix = '/api'

    from app.customer import customer_bp
    app.register_blueprint(customer_bp, url_prefix=f"{api_prefix}/customer")

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix=f"{api_prefix}/user")

    from app.scheduling import scheduling_bp
    app.register_blueprint(scheduling_bp, url_prefix=f"{api_prefix}/scheduling")

    from app.services import services_bp
    app.register_blueprint(services_bp)

    from app.negotiation import negotiation_bp
    app.register_blueprint(negotiation_bp, url_prefix=f"{api_prefix}/negotiation")

    from app.purchasing import purchasing_bp
    app.register_blueprint(purchasing_bp, url_prefix=f"{api_prefix}/purchasing")
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix=f"{api_prefix}/auth")

    from app.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix=f"{api_prefix}/inventory")

    # Registering Services
    from app.negotiation.services import NegotiationService
    app.negotiation_service = NegotiationService()

    from app.inventory.services import InventoryService
    app.inventory_service = InventoryService()

    from app.customer.services import CustomerServices
    app.customer_service = CustomerServices()

    from app.user.services import UserServices
    app.user_service = UserServices()

    @app.before_request
    def before_request():
        g.negotiation_service = current_app.negotiation_service
        g.inventory_service = current_app.inventory_service
        g.customer_service = current_app.customer_service
        g.user_service = current_app.user_service

    return app