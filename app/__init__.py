from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)


    # Registering Blueprints
    from app.customer import customer_bp
    app.register_blueprint(customer_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    from app.services import services_bp
    app.register_blueprint(services_bp)

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

    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    # Registering Services
    from app.services.scheduling_service import ScheduleService
    app.schedule_service = ScheduleService()

    from app.services.negotiation_service import NegotiationService
    app.negotiation_service = NegotiationService()

    from app.services.purchasing_service import PurchasingService
    app.purchasing_service = PurchasingService()

    from app.services.inventory_service import InventoryService
    app.inventory_service = InventoryService()

    @app.before_request
    def before_request():
        g.schedule_service = current_app.schedule_service
        g.negotiation_service = current_app.negotiation_service
        g.purchasing_service = current_app.purchasing_service
        g.inventory_service = current_app.inventory_service

    return app