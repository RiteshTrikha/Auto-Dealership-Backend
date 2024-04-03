from flask_restx import Resource,fields, Namespace
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask import request,jsonify
from ext import db

user_ns = Namespace('user', description='User related operations')


user_models=user_ns.model("User",{
    "id":fields.Integer(),
    "email":fields.String(),
    "f_name":fields.String(),
    "l_name":fields.String(),
    "password":fields.String(),
    "is_admin":fields.Boolean(),
    "is_active":fields.Boolean()
})



@user_ns.route('/user')
class UsersResource(Resource):
    @user_ns.marshal_list_with(user_models)
    def get(self):
        users = User.query.all()
        return users
    
    @user_ns.expect(user_models)
    @user_ns.marshal_with(user_models)
    def post(self):
        data = request.get_json()
        if isinstance(data, list):  # Check if data is a list of users
            new_users = []
            for user_data in data:
                new_user = User(**user_data)
                new_user.save()
                new_users.append(new_user)
            return new_users, 201
        else:  # If data is a single user object
            new_user = User(**data)
            new_user.save()
            return new_user, 201


@user_ns.route('/user/<int:id>')
class UserResources(Resource):
    @user_ns.marshal_list_with(user_models)
    def get(self,id):
        user=User.query.get(id)
        return user
    
    @user_ns.marshal_with(user_models)
    def put(self,id):
        user_to_update=User.query.get_or_404(id)
        data=request.get_json()
        user_to_update.update(email=data.get("email"),
                    f_name=data.get("f_name"),
                    l_name=data.get("l_name"),
                    password=data.get("password"))
        return user_to_update
        
    @user_ns.marshal_with(user_models)
    def delete(self,id):
        user_to_delete=User.query.get_or_404(id)
        user_to_delete.delete()
        return {"message":"User deleted"}