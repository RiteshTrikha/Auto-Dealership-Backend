from flask import current_app
from .models import User
from app.exceptions import ExposedException
from app import db

class UserServices:
        
    def create(self, role_id, email, password, first_name, last_name):
        try:
            user_id = User.create(role_id, email, password, first_name, last_name)
            db.session.commit()
            return user_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise e
        
    def get_user_details(self, user_id):
        try:
            user = User.get_user_by_user_id(user_id)
            user_dict = {
                'user_id': user_id,
                'role_id': user.role_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'create_time': user.create_time
            }
            return user_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        