from flask import current_app
from .models import CreditReport, Customer, CustomerVehicle
from app.exceptions import ExposedException
from app import db
class CustomerServices:

    def create(self, first_name, last_name, email, password, birth_date, drivers_license):
        try:
            customer = Customer.create(first_name, last_name, email, password, birth_date, drivers_license)
            db.session.commit()
            return customer.customer_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def get_by_email(self, email):
        try:
            customer = Customer.get_by_email(email)
            return customer
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def update_customer_status(self, customer_id, status):
        try:
            customer = Customer.update_customer_status(customer_id, status)
            db.session.commit()
            return customer
        except Exception as e:
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

######## Customer Vehicle Services ########
        
    def create_customer_vehicle(self, customer_id, year, make, model, vin):
        try:
            vehicle = CustomerVehicle.create_vehicle(vin, year, make, model, customer_id)
            db.session.commit()
            return vehicle
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def get_vehicle(self, customer_vehicle_id):
        try:
            vehicle = CustomerVehicle.get_vehicle(customer_vehicle_id)
            return vehicle
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def get_vehicles(self, customer_id):
        try:
            vehicles = CustomerVehicle.get_vehicles(customer_id)
            return vehicles
        except Exception as e:
            current_app.logger.exception(e)
            raise e
    
    def update_vehicle(self, customer_vehicle_id, year, make, model):
        try:
            vehicle = CustomerVehicle.get_vehicle(customer_vehicle_id)
            if vehicle is None:
                raise ExposedException('Vehicle not found', 404)
            vehicle.year = year
            vehicle.make = make
            vehicle.model = model
            db.session.commit()
            return vehicle
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
######## Customer Credit Report Services ########

    def create_credit_report(self, customer_id, score, apy):
        try:
            credit_report = CreditReport.create_credit_report(customer_id, score, apy)
            db.session.commit()
            return credit_report
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def get_credit_report_by_customer(self, customer_id):
        try:
            credit_report = CreditReport.get_credit_report_by_customer(customer_id)
            return credit_report
        except Exception as e:
            current_app.logger.exception(e)
            raise e
    
    def delete_vehicle(self, customer_vehicle_id):
        try:
            vehicle = CustomerVehicle.get_vehicle(customer_vehicle_id)
            if vehicle is None:
                raise ExposedException('Vehicle not found', 404)
            db.session.delete(vehicle)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        