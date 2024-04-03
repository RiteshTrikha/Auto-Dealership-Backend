from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource,fields
from config import DevConfig
from models import User
from ext import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from auth import auth_ns
from users import user_ns

def create_app(config):
    app = Flask(__name__)

    app.config.from_object(DevConfig)
    db.init_app(app)
    jwt = JWTManager(app)


    migrate=Migrate(app,db)

    api = Api(app,doc='/docs')

    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)

    @app.shell_context_processor
    def make_shell_context():
        return {"db":db,
                "User":User}
    
    return app