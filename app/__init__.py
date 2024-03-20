from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
from services.scheduling_service import ScheduleService
from services.negotiation_service import NegotiationService
from services.purchasing_service import PurchasingService

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    # Registering Services
    app.schedule_service = ScheduleService()
    app.negotiation_service = NegotiationService()
    app.purchasing_service = PurchasingService()


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

    @app.before_request
    def before_request():
        g.schedule_service = current_app.schedule_service
        g.negotiation_service = current_app.negotiation_service
        g.purchasing_service = current_app.purchasing_service

    return app