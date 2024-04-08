from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app import db
from app.exceptions import ExposedException

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
                raise ExposedException('Email already exists', 400)
            # create customer
            customer_id = g.customer_service.create(first_name=first_name, last_name=last_name, 
                                                    email=email, password=generate_password_hash(password), 
                                                    birth_date=birth_date, 
                                                    drivers_license=drivers_license)
            return {'customer_id': customer_id}
        except ExposedException as e:
            raise e
        except Exception as e:
            current_app.logger.error(str(e))
            raise e
        
    def login_customer(self, email, password):
        try:
            # get customer by email
            customer = g.customer_service.get_by_email(email)
            # check if customer exists
            if not customer or not check_password_hash(customer.password, password):
                raise ExposedException('Invalid email or password', 400)
            # create jwt token
            access_token = create_access_token(identity=customer.customer_id)
            return {'access_token': access_token}
        except ExposedException as e:
            raise e
        except Exception as e:
            current_app.logger.error(str(e))
            raise e
    
        
        
