from flask import current_app, g
from customer.models import Customer
from user.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app import db
from exceptions import ExposedException

# customer_id = Column(INTEGER, primary_key=True, unique=True)
# first_name = Column(String(32), nullable=False)
# last_name = Column(String(32))
# email = Column(String(254))
# password = Column(String(72), nullable=False)
# ssn = Column(String(11))
# birth_date = Column(Date)
# drivers_license = Column(String(16))
# address_id = Column(Integer)
# create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
# status = Column(Integer, nullable=False)

class AuthService:
    def register_customer(self, first_name, last_name, email, password, birth_date, drivers_license=None):
        try:
            # check if email exists
            if g.customer_service.get_by_email(email):
                return ExposedException('Email already exists', 400)
            # create customer
            customer_id = g.customer_service.create(first_name, last_name, email, generate_password_hash(password), birth_date, drivers_license)
            return customer_id
        except Exception as e:
            raise e
        
    def login_customer(self, email, password):
        try:
            # get customer by email
            customer = g.customer_service.get_by_email(email)
            # check if customer exists
            if not customer or not check_password_hash(customer.password, password):
                return ExposedException('Invalid email or password', 400)
            # login customer
            login_user(customer)
        except Exception as e:
            raise e
        
    def logout_customer(self):
        try:
            logout_user()
        except Exception as e:
            raise e
    
        
        
