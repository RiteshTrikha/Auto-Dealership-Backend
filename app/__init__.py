from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flasgger import Swagger
from flask_cors import CORS
from app.error_handlers import register_error_handlers
from flask_login import LoginManager
import logging


db = SQLAlchemy()
swagger = Swagger()
cors = CORS()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    swagger.init_app(app)
    cors.init_app(app)

    # Registering Error Handlers
    register_error_handlers(app)
    login_manager.init_app(app)

    # login
    from app.user.models import User
    from app.customer.models import Customer

    admin_permission = 

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(user_id))

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

    @app.before_request
    def before_request():
        g.negotiation_service = current_app.negotiation_service
        g.inventory_service = current_app.inventory_service

    return app