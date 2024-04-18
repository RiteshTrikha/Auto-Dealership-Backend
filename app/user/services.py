from flask import current_app
from .models import User
from app.exceptions import ExposedException
from app import db

class UserServices:
        
    def get_by_email(self, email):
        try:
            customer = User.get_by_email(email)
            return customer
        except Exception as e:
            current_app.logger.error(str(e))
            raise e
        