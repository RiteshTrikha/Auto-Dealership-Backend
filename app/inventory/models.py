from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()
metadata = Base.metadata

class RetailItem(Base):
    __tablename__ = 'retail_item'

    retail_item_id = Column(INTEGER, primary_key=True, unique=True)
    name = Column(String(45))
    price = Column(INTEGER)
    description = Column(String(254))

class Vehical(Base):
    __tablename__ = 'vehical'

    class VehicalStatus(Enum):
        INACTIVE = 0
        AVAILABLE = 1
        SOLD = 2

    vehical_id = Column(INTEGER, primary_key=True, unique=True)
    vin = Column(String(17), nullable=False)
    price = Column(INTEGER)
    year = Column(String(4))
    make = Column(String(45))
    model = Column(String(45))
    miles = Column(INTEGER)
    mpg = Column(INTEGER)
    color = Column(String(45))
    fuel_type = Column(String(45))
    transmission = Column(String(45))
    image = Column(String(254))
    vehical_status = Column(INTEGER)

    # functions
    def serialize(self):
        return {
            'vehical_id': self.vehical_id,
            'vin': self.vin,
            'price': self.price,
            'year': self.year,
            'make': self.make,
            'model': self.model,
            'miles': self.miles,
            'mpg': self.mpg,
            'color': self.color,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'vehical_status': self.vehical_status
        }
    
    @classmethod
    def get_all_vehicles(cls):
        try:
            vehicles = db.session.query(Vehical).all()
            return vehicles
        except Exception as e:
            raise e
        
    @classmethod
    def get_vehicle(cls, vehical_id):
        try:
            vehicle = db.session.query(Vehical).filter_by(vehical_id=vehical_id).first()
            return vehicle
        except Exception as e:
            raise e
        
    @classmethod    
    def get_top_5_vehicles(cls):
        try:
            vehicles = db.session.query(Vehical).limit(5).all()
            return vehicles
        except Exception as e:
            raise e
        
    def create_vehicle(self, vin, price, year, make, model, miles, mpg, color, fuel_type, transmission, vehical_status):
        try:
            vehicle = Vehical(vin=vin, price=price, year=year, make=make, model=model, miles=miles, mpg=mpg, color=color, fuel_type=fuel_type, transmission=transmission, vehical_status=vehical_status)
            db.session.add(vehicle)
            db.session.commit()
            return vehicle
        except Exception as e:
            raise e
        
    def update_vehicle(self, vehical_id, vin, price, year, make, model, miles, mpg, color, fuel_type, transmission, vehical_status):
        try:
            vehicle = db.session.query(Vehical).filter_by(vehical_id=vehical_id).first()
            vehicle.vin = vin
            vehicle.price = price
            vehicle.year = year
            vehicle.make = make
            vehicle.model = model
            vehicle.miles = miles
            vehicle.mpg = mpg
            vehicle.color = color
            vehicle.fuel_type = fuel_type
            vehicle.transmission = transmission
            vehicle.vehical_status = vehical_status
            db.session.commit()
            return vehicle
        except Exception as e:
            raise e
        
    def deactivate_vehicle(self, vehical_id):
        try:
            vehicle = db.session.query(Vehical).filter_by(vehical_id=vehical_id).first()
            vehicle.vehical_status = 0
            db.session.commit()
            return vehicle
        except Exception as e:
            raise e
        
    
    