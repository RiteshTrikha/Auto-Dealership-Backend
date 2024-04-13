from flask import current_app
from .models import Customer, CreditReport
from app.exceptions import ExposedException
from app import db
class CustomerServices:

    def create(self, first_name, last_name, email, password, birth_date, drivers_license):
        try:
            customer_id = Customer.create(first_name, last_name, email, password, birth_date, drivers_license)
            
            db.session.commit()
            return customer_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise e
        
    def get_by_email(self, email):
        try:
            customer = Customer.get_by_email(email)
            return customer
        except Exception as e:
            current_app.logger.error(str(e))
            raise e
