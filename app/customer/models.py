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

    credit_report = relationship('CreditReport', uselist=False)
    customer_vehicle = relationship('CustomerVehicle', backref='customer')
    addons = relationship('CustomerAddon', backref='customer')

    # create customer
    @classmethod
    def create(cls, first_name, last_name, email, password, birth_date, 
               drivers_license):
        try:
            # create customer
            customer = Customer(first_name=first_name, last_name=last_name, email=email, password=password,
                                birth_date=birth_date, drivers_license=drivers_license, status=1)
            db.session.add(customer)
            return customer
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
        
    @classmethod
    def update_customer_status(cls, customer_id, status):
        try:
            customer = db.session.query(Customer).filter(Customer.customer_id == customer_id).first()
            customer.status = status
            return customer
        except Exception as e:
            raise e

        
class CreditReport(db.Model):
    __tablename__ = 'credit_report'

    credit_report_id = Column(INTEGER, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True, unique=True)
    score = Column(INTEGER, nullable=False)
    apr = Column(Float, nullable=False)
    max_loan = Column(Float, nullable=False)

    customer = relationship('Customer')

    def save_credit_score(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @classmethod
    def get_credit_report_by_customer(cls, customer_id):
        try:
            credit_report = db.session.query(CreditReport).filter(CreditReport.customer_id == customer_id).first()
            return credit_report
        except Exception as e:
            raise e
        
    @classmethod
    def create_credit_report(cls, customer_id, score, apr):
        try:
            credit_report = CreditReport(customer_id=customer_id, score=score, apr=apr)
            db.session.add(credit_report)
            return credit_report
        except Exception as e:
            raise e


class CustomerVehicle(db.Model):
    __tablename__ = 'customer_vehicle'

    customer_vehicle_id = Column(INTEGER, primary_key=True, unique=True)
    vin = Column(String(45), nullable=False, unique=True)
    year = Column(INTEGER, server_default=text("2024"))
    make = Column(String(254))
    model = Column(String(254))
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)

    def to_dict(self):
        return {
            'customer_vehicle_id': self.customer_vehicle_id,
            'vin': self.vin,
            'year': self.year,
            'make': self.make,
            'model': self.model,
            'customer_id': self.customer_id
        }

    @classmethod
    def create_vehicle(cls, vin, year, make, model, customer_id):
        try:
            vehicle = CustomerVehicle(vin=vin, year=year, make=make, model=model, customer_id=customer_id)
            db.session.add(vehicle)
            return vehicle
        except Exception as e:
            raise e

    @classmethod    
    def get_vehicle(cls, customer_vehicle_id):
        try:
            vehicle = db.session.query(CustomerVehicle).filter(CustomerVehicle.customer_vehicle_id == customer_vehicle_id).first()
            return vehicle
        except Exception as e:
            raise e

    @classmethod    
    def get_vehicles(cls, customer_id):
        try:
            vehicles = db.session.query(CustomerVehicle).filter(CustomerVehicle.customer_id == customer_id).all()
            return vehicles
        except Exception as e:
            raise e

    @classmethod
    def update_vehicle(cls, customer_vehicle_id, year, make, model):
        try:
            vehicle = db.session.query(CustomerVehicle).filter(CustomerVehicle.customer_vehicle_id == customer_vehicle_id).first()
            vehicle.year = year
            vehicle.make = make
            vehicle.model = model
            return vehicle
        except Exception as e:
            raise e
        
    @classmethod
    def delete_vehicle(cls, customer_vehicle_id):
        try:
            vehicle = db.session.query(CustomerVehicle).filter(CustomerVehicle.customer_vehicle_id == customer_vehicle_id).first()
            db.session.delete(vehicle)
        except Exception as e:
            raise e
        

class CustomerAddon(db.Model):
    __tablename__ = 'customer_addon'

    customer_addon_id = Column(INTEGER, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    customer_vehicle_id = Column(ForeignKey('customer_vehicle.customer_vehicle_id'), index=True)
    addon_id = Column(ForeignKey('addon.addon_id'), nullable=False, index=True)

    addon = relationship('app.inventory.models.Addon', uselist=False, backref='customer_addon')

    @classmethod
    def create_customer_addon(cls, customer_id, addon_id, customer_vehicle_id):
        try:
            customer_addon = CustomerAddon(customer_id=customer_id, addon_id=addon_id,
                                             customer_vehicle_id=customer_vehicle_id)
            db.session.add(customer_addon)
            return customer_addon
        except Exception as e:
            raise e

    @classmethod
    def get_by_customer(cls, customer_id):
        try:
            customer_addons = db.session.query(CustomerAddon).filter(CustomerAddon.customer_id == customer_id).all()
            return customer_addons
        except Exception as e:
            raise e

    @classmethod
    def get_by_addon(cls, addon_id):
        try:
            customer_addons = db.session.query(CustomerAddon).filter(CustomerAddon.addon_id == addon_id).all()
            return customer_addons
        except Exception as e:
            raise e