from flask import request, jsonify, current_app
from .models import Vehical, Service
from app.exceptions import ExposedException
from app import db

class InventoryService:

    # vehical_id = Column(INTEGER, primary_key=True, unique=True)
    # vin = Column(String(17), nullable=False)
    # price = Column(INTEGER)
    # year = Column(String(4))
    # make = Column(String(45))
    # model = Column(String(45))
    # miles = Column(INTEGER)
    # mpg = Column(INTEGER)
    # color = Column(String(45))
    # fuel_type = Column(String(45))
    # transmission = Column(String(45))
    # image = Column(String(254))
    # vehical_status = Column(INTEGER)
    
    def create_vehical(self, vin, price, year, make, model, miles, mpg, color, fuel_type, 
                       transmission, image, vehical_status=Vehical.VehicalStatus.AVAILABLE.value):
        try:
            vehical = Vehical.create_vehical(vin=vin, price=price, year=year, make=make, 
                                             model=model, miles=miles, mpg=mpg, color=color, 
                                             fuel_type=fuel_type, transmission=transmission,
                                             image=image, vehical_status=vehical_status)
            db.session.commit()
            return { 'vehical_id': vehical.vehical_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def update_vehical(self, vehical_id, vin, price, year, make, model, miles, mpg, 
                       color, fuel_type, transmission, image):
        try:
            vehical = Vehical.update_vehical(vehical_id, vin, price, year, make, model, miles, mpg, 
                                             color, fuel_type, transmission, image)
            db.session.commit()
            return { 'vehical_id': vehical.vehical_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def change_vehical_status(self, vehical_id, vehical_status):
        try:
            if vehical_status not in [status.value for status in Vehical.VehicalStatus]:
                raise ExposedException('Invalid vehical status', code=400)
            vehical = Vehical.update_vehical(vehical_id, vehical_status=vehical_status)
            db.session.commit()
            return { 'vehical_id': vehical.vehical_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
           
    def get_vehical(self, vehical_id):
        try:
            vehical = Vehical.get_vehical(vehical_id)
            if not vehical:
                raise ExposedException('vehical not found', code=404)
            return {
                'vehical_id': vehical.vehical_id,
                'vin': vehical.vin,
                'price': vehical.price,
                'year': vehical.year,
                'make': vehical.make,
                'model': vehical.model,
                'miles': vehical.miles,
                'mpg': vehical.mpg,
                'color': vehical.color,
                'fuel_type': vehical.fuel_type,
                'transmission': vehical.transmission,
                'image': vehical.image,
                'vehical_status': vehical.vehical_status
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
            
    
    def get_vehicals(self, page, limit, query):
        try:
            vehicals, num_of_pages = Vehical.get_vehicals(page=page, limit=limit, query=query)
            if vehicals == []:
                raise ExposedException('No vehicals found', code=404)
            json_dict = {
                    'num_of_pages': num_of_pages,
                    'num_of_results': num_of_records,
                    'page': page,
                    'vehicals': 
                    [{
                        'vehical_id': vehical.vehical_id,
                        'price': vehical.price,
                        'year': vehical.year,
                        'make': vehical.make,
                        'model': vehical.model,
                        'miles': vehical.miles,
                        'mpg': vehical.mpg,
                        'color': vehical.color,
                        'fuel_type': vehical.fuel_type,
                        'transmission': vehical.transmission,
                        'image': vehical.image,
                        'vehical_status': vehical.vehical_status
                    } for vehical in vehicals],
                }
            return json_dict
        except Exception as e:
            current_app.logger.exception(e) # TODO: switch all loggers to exception instead of error and remove the str()
            raise e
        
    def get_top_5_vehicals(self):
        try:
            vehicals = Vehical.get_top_5_vehicals()
            if vehicals == []:
                raise ExposedException('No vehicals found', code=404)
            return [{
                'vehical_id': vehical.vehical_id,
                'price': vehical.price,
                'year': vehical.year,
                'make': vehical.make,
                'model': vehical.model,
                'miles': vehical.miles,
                'mpg': vehical.mpg,
                'color': vehical.color,
                'fuel_type': vehical.fuel_type,
                'transmission': vehical.transmission,
                'image': vehical.image,
                'vehical_status': vehical.vehical_status
            } for vehical in vehicals]
        except Exception as e:
            current_app.logger.exception(e)
            raise e