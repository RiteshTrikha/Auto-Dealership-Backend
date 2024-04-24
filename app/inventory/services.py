from flask import request, jsonify, current_app
from .models import Vehicle, Service
from app.exceptions import ExposedException
from app import db

class InventoryService:

    # vehicle_id = Column(INTEGER, primary_key=True, unique=True)
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
    # vehicle_status = Column(INTEGER)

    # service services

    def create_service(self, service_type, price, description):
        try:
            service = Service.create_service(service_type=service_type, price=price, description=description)
            db.session.commit()
            return { 'service_id': service.service_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def update_service(self, service_id, service_type, price, description):
        try:
            service = Service.update_service(service_id=service_id, service_type=service_type, 
                                             price=price, description=description)
            db.session.commit()
            return { 'service_id': service.service_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
    
    def change_service_status(self, service_id, status):
        try:
            if status not in [status.value for status in Service.ServiceStatus]:
                raise ExposedException('Invalid service status', code=400)
            service = Service.update_service_status(service_id, status)
            db.session.commit()
            return { 'service_id': service.service_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def get_service(self, service_id):
        try:
            service = Service.get_service(service_id)
            if not service:
                raise ExposedException('Service not found', code=404)
            return {
                'service_id': service.service_id,
                'service_type': service.service_type,
                'price': service.price,
                'description': service.description,
                'status': Service.ServiceStatus(service.status).name
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def get_services(self):
        try:
            services = Service.get_services()
            if services == []:
                raise ExposedException('No services found', code=404)
            return [{
                'service_id': service.service_id,
                'service_type': service.service_type,
                'price': service.price,
                'description': service.description,
                'status': Service.ServiceStatus(service.status).name
            } for service in services]
        except Exception as e:
            current_app.logger.exception(e)
            raise e


    # vehicle services
    
    def create_vehicle(self, vin, price, year, make, model, miles, mpg, color, fuel_type, 
                       transmission, image, vehicle_status=Vehicle.VehicleStatus.AVAILABLE.value):
        try:
            vehicle = Vehicle.create_vehicle(vin=vin, price=price, year=year, make=make, 
                                             model=model, miles=miles, mpg=mpg, color=color, 
                                             fuel_type=fuel_type, transmission=transmission,
                                             image=image, vehicle_status=vehicle_status)
            db.session.commit()
            return { 'vehicle_id': vehicle.vehicle_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def update_vehicle(self, vehicle_id, vin, price, year, make, model, miles, mpg, 
                       color, fuel_type, transmission, image):
        try:
            vehicle = Vehicle.update_vehicle(vehicle_id, vin, price, year, make, model, miles, mpg, 
                                             color, fuel_type, transmission, image)
            db.session.commit()
            return { 'vehicle_id': vehicle.vehicle_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def change_vehicle_status(self, vehicle_id, vehicle_status):
        try:
            if vehicle_status not in [status.value for status in vehicle.VehicleStatus]:
                raise ExposedException('Invalid vehicle status', code=400)
            vehicle = Vehicle.update_vehicle(vehicle_id, vehicle_status=vehicle_status)
            db.session.commit()
            return { 'vehicle_id': vehicle.vehicle_id }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
           
    def get_vehicle(self, vehicle_id):
        try:
            vehicle = Vehicle.get_vehicle(vehicle_id)
            if not vehicle:
                raise ExposedException('Vehicle not found', code=404)
            return {
                'vehicle_id': vehicle.vehicle_id,
                'vin': vehicle.vin,
                'price': vehicle.price,
                'year': vehicle.year,
                'make': vehicle.make,
                'model': vehicle.model,
                'miles': vehicle.miles,
                'mpg': vehicle.mpg,
                'color': vehicle.color,
                'fuel_type': vehicle.fuel_type,
                'transmission': vehicle.transmission,
                'image': vehicle.image,
                'vehicle_status': vehicle.vehicle_status
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
            
    
    def get_vehicals(self, page, limit, query):
        try:
            vehicles, num_of_pages, num_of_records = Vehicle.get_vehicles(page=page, limit=limit, query=query)
            if vehicles == []:
                raise ExposedException('No vehicles found', code=404)
            json_dict = {
                    'num_of_pages': num_of_pages,
                    'num_of_results': num_of_records,
                    'page': page,
                    'vehicals': 
                    [{
                        'vehicle_id': vehicle.vehicle_id,
                        'price': vehicle.price,
                        'year': vehicle.year,
                        'make': vehicle.make,
                        'model': vehicle.model,
                        'miles': vehicle.miles,
                        'mpg': vehicle.mpg,
                        'color': vehicle.color,
                        'fuel_type': vehicle.fuel_type,
                        'transmission': vehicle.transmission,
                        'image': vehicle.image,
                        'vehicle_status': vehicle.vehicle_status
                    } for vehicle in vehicles],
                }
            return json_dict
        except Exception as e:
            current_app.logger.exception(e) # TODO: switch all loggers to exception instead of error and remove the str()
            raise e
        
    def get_top_5_vehicals(self):
        try:
            vehicles = Vehicle.get_top_5_vehicles()
            if vehicles == []:
                raise ExposedException('No vehicles found', code=404)
            return [{
                'vehicle_id': vehicle.vehicle_id,
                'price': vehicle.price,
                'year': vehicle.year,
                'make': vehicle.make,
                'model': vehicle.model,
                'miles': vehicle.miles,
                'mpg': vehicle.mpg,
                'color': vehicle.color,
                'fuel_type': vehicle.fuel_type,
                'transmission': vehicle.transmission,
                'image': vehicle.image,
                'vehicle_status': vehicle.vehicle_status
            } for vehicle in vehicles]
        except Exception as e:
            current_app.logger.exception(e)
            raise e