from flask import current_app
from .models import User
from app.exceptions import ExposedException
# import password hashing library
from werkzeug.security import generate_password_hash
from app import db

class UserServices:
        
    def get_by_email(self, email):
        try:
            customer = User.get_by_email(email)
            return customer
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    def create_user(self, email, password, first_name, last_name, role_id):
        try:
            if self.get_by_email(email):
                raise ExposedException('User already exists')
            user = User.create_user(email=email, password=generate_password_hash(password), first_name=first_name, last_name=last_name, role_id=role_id)
            return {
                'user_id': user.user_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role_id': user.role_id,
                'role': user.role.role
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def update_user(self, user_id, email, password, first_name, last_name, role_id):
        try:
            user = User.update_user(user_id=user_id, email=email, 
                                    password=generate_password_hash(password), 
                                    first_name=first_name, last_name=last_name, 
                                    role_id=role_id)
            return {
                'user_id': user.user_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role_id': user.role_id,
                'role': user.role.role
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def get_by_id(self, user_id):
        try:
            user = User.get_by_id(user_id)
            return {
                'user_id': user.user_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role_id': user.role_id,
                'role': user.role.role,
                'is_active': user.is_active
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def get_all(self):
        try:
            users = User.get_all()
            return {
                'users': [{
                    'user_id': user.user_id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role_id': user.role_id,
                    'role': user.role.role,
                    'is_active': user.is_active
                } for user in users]
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        

    def deactivate_user(self, user_id):
        try:
            user = User.deactivate_user(user_id)
            return {
                'user_id': user.user_id,
                'is_active': user.is_active
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def activate_user(self, user_id):
        try:
            user = User.activate_user(user_id)
            return {
                'user_id': user.user_id,
                'is_active': user.is_active
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        