from flask import current_app
from .models import Customer
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

    def get_customer_details(self, customer_id):
        try:
            customer = Customer.get_customer(customer_id)
            customer_dict = {
                'customer_id': customer_id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'ssn': customer.ssn,
                'birth_date': customer.birth_date,
                'drivers_license': customer.drivers_license,
                'address_id': customer.address_id,
                'create_time': customer.create_time,
                'status': customer.status
            }
            return customer_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        