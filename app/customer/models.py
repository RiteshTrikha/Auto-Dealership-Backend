from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import Enum


class Customer(db.Model):  
    __tablename__ = 'customer'

    class CustomerStatus(Enum):
        ACTIVE = 1
        INACTIVE = 2

    customer_id = Column(INTEGER, primary_key=True, unique=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32))
    email = Column(String(254))
    password = Column(String(256), nullable=False)
    ssn = Column(String(11))
    birth_date = Column(Date)
    drivers_license = Column(String(16))
    address_id = Column(Integer)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer, nullable=False)

    # create customer
    @classmethod
    def create(cls, first_name, last_name, email, password, birth_date, 
               drivers_license):
        try:
            # create customer
            customer = Customer(first_name=first_name, last_name=last_name, email=email, password=password, 
                                birth_date=birth_date, drivers_license=drivers_license, status=1)
            db.session.add(customer)
            return customer.customer_id
        except Exception as e:
            raise e
        
    # get customer by email
    @classmethod
    def get_by_email(cls, email):
        try:
            customer =  db.session.query(Customer).filter(Customer.email == email).first()
            return customer
        except Exception as e:
            raise e
    
    @classmethod
    def get_customer(cls, customer_id):
        try:
            customer = db.session.query(Customer).filter(Customer.customer_id == customer_id).first()
            return customer
        except Exception as e:
            raise e

        
class CreditReport(db.Model):
    __tablename__ = 'credit_report'

    credit_report_id = Column(INTEGER, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    score = Column(INTEGER, nullable=False)
    apy = Column(Float, nullable=False)

    customer = relationship('Customer')

    def save_credit_score(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class CustomerVehical(db.Model):
    __tablename__ = 'customer_vehical'

    customer_vehical_id = Column(INTEGER, primary_key=True, unique=True)
    vin = Column(String(45))
    year = Column(String(4))
    make = Column(String(254))
    model = Column(String(254))
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)

    customer = relationship('Customer')