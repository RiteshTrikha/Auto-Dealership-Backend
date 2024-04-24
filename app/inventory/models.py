from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import Enum

# class Service(db.Model):
#     __tablename__ = 'service'

#     class ServiceStatus(Enum):
#         INACTIVE = 0
#         ACTIVE = 1

#     service_id = Column(INTEGER, primary_key=True, unique=True)
#     service_type = Column(String(45))
#     price = Column(INTEGER)
#     description = Column(String(254))
#     status = Column(INTEGER, server_default=text("'1'"))

#     @classmethod
#     def get_services(cls):
#         try:
#             services = db.session.query(Service).all()
#             return services
#         except Exception as e:
#             raise e
        
#     @classmethod
#     def get_service(cls, service_id):
#         try:
#             service = db.session.query(Service).filter_by(service_id=service_id).first()
#             return service
#         except Exception as e:
#             raise e
        
#     @classmethod
#     def create_service(cls, service_type, price, description):
#         try:
#             service = Service(service_type=service_type, price=price, description=description)
#             db.session.add(service)
#             return service
#         except Exception as e:
#             raise e
    
#     @classmethod
#     def update_service(cls, service_id, service_type=None, price=None, description=None):
#         try:
#             service = db.session.query(Service).filter_by(service_id=service_id).first()
#             if service_type:
#                 service.service_type = service_type
#             if price:
#                 service.price = price
#             if description:
#                 service.description = description
#             return service
#         except Exception as e:
#             raise e
        
#     @classmethod
#     def update_service_status(cls, service_id, status):
#         try:
#             service = db.session.query(Service).filter_by(service_id=service_id).first()
#             service.status = status
#             return service
#         except Exception as e:
#             raise e
        
#copied from scheduling
class Service(db.Model):
    __tablename__ = 'service'

    class ServiceStatus(Enum):
        INACTIVE = 0
        ACTIVE = 1

    service_id = Column(INTEGER, primary_key=True, unique=True)
    service_type = Column(String(255), nullable=False)
    price = Column(INTEGER, nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(INTEGER, server_default=text("'1'"))


    #get service by service id
    @classmethod
    def get_service_by_service_id(cls, service_id):
        try:
            return db.session.query(Service).filter(Service.service_id == service_id).first()
        except Exception as e:
            raise e
    
    #get service by service_type
    @classmethod
    def get_service_by_service_type(cls, service_type):
        try:
            return db.session.query(Service).filter(Service.service_type == service_type).first()
        except Exception as e:
            raise e

    #get all services
    @classmethod
    def get_all_services(cls):
        try:
            return db.session.query(Service).all()
        except Exception as e:
            raise e

    #create service
    @classmethod
    def create_service(self, service_type, price, description):
        try:
            service = Service(service_type=service_type, price=price, description=description)
            db.session.add(service)
            return service
        except Exception as e:
            raise e

    @classmethod
    def update_service_status(cls, service_id, status):
        try:
            service = db.session.query(Service).filter_by(service_id=service_id).first()
            service.status = status
            return service
        except Exception as e:
            raise e    

    #update service
    @classmethod
    def update_service(self, service_id, service_type, price, description, status):
        try:
            service = db.session.query(Service).filter(Service.service_id == service_id).first()
            service.service_type = service_type
            service.price = price
            service.description = description
            service.status = status
            return service
        except Exception as e:
            raise e



class Vehical(db.Model):
    __tablename__ = 'vehical'

    class VehicalStatus(Enum):
        INACTIVE = 0
        AVAILABLE = 1
        SOLD = 2
        RESERVED = 3

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
    
    @classmethod
    def get_vehicals(cls, page=1, limit=10, query=None):
        try:
            query_obj = db.session.query(Vehical)
            if query:
                query_obj = query_obj.filter(
                    Vehical.year.like(f'%{query}%') | 
                    Vehical.make.like(f'%{query}%') | 
                    Vehical.model.like(f'%{query}%') | 
                    Vehical.color.like(f'%{query}%') | 
                    Vehical.fuel_type.like(f'%{query}%') | 
                    Vehical.transmission.like(f'%{query}%')
                )
            
            num_of_records = query_obj.count()
            num_of_pages = num_of_records // limit
            if num_of_records % limit > 0:
                num_of_pages += 1
            
            if page > num_of_pages:
                page = max(1, num_of_pages)
            
            start_index = (page - 1) * limit
            vehicals = query_obj.slice(start_index, start_index + limit).all()

            return vehicals, num_of_pages, num_of_records
        except Exception as e:
            raise e
        
    @classmethod
    def get_vehical(cls, vehical_id):
        try:
            vehical = db.session.query(Vehical).filter_by(vehical_id=vehical_id).first()
            return vehical
        except Exception as e:
            raise e
        
    @classmethod    
    def get_top_5_vehicals(cls):
        try:
            vehicals = db.session.query(Vehical).limit(5).all()
            return vehicals
        except Exception as e:
            raise e
    
    @classmethod
    def create_vehical(cls, vin, price, year, make, model, miles, mpg, color, 
                       fuel_type, transmission, image, vehical_status):
        try:
            vehical = Vehical(vin=vin, price=price, year=year, make=make, 
                              model=model, miles=miles, mpg=mpg, color=color, 
                              fuel_type=fuel_type, transmission=transmission, image=image, 
                              vehical_status=vehical_status)
            db.session.add(vehical)
            return vehical
        except Exception as e:
            raise e
    
    @classmethod
    def update_vehical(cls, vehical_id, vin=None, price=None, year=None, 
                       make=None, model=None, miles=None, mpg=None, color=None, 
                       fuel_type=None, transmission=None, image=None, vehical_status=None):
        try:
            vehical = db.session.query(Vehical).filter_by(vehical_id=vehical_id).first()
            if vin:
                vehical.vin = vin
            if price: 
                vehical.price = price
            if year:
                vehical.year = year
            if make:
                vehical.make = make
            if model:
                vehical.model = model
            if miles:
                vehical.miles = miles
            if mpg:
                vehical.mpg = mpg
            if color:
                vehical.color = color
            if fuel_type:
                vehical.fuel_type = fuel_type
            if transmission:
                vehical.transmission = transmission
            if image:
                vehical.image = image
            if vehical_status:
                vehical.vehical_status = vehical_status
            return vehical
        except Exception as e:
            raise e
        
    def update_vehical_status(self, status):
        try:
            self.vehical_status = status
            return self
        except Exception as e:
            raise e

class Addon(db.Model):
    __tablename__ = 'addon'

    class AddonStatus(Enum):
        INACTIVE = 0
        ACTIVE = 1

    addon_id = Column(INTEGER, primary_key=True, unique=True)
    addon_name = Column(String(45))
    price = Column(INTEGER)
    description = Column(String(254))
    status = Column(INTEGER, server_default=text("'1'"))

    @classmethod
    def get_addons(cls):
        try:
            addons = db.session.query(Addon).all()
            return addons
        except Exception as e:
            raise e
        
    @classmethod
    def get_addon(cls, addon_id):
        try:
            addon = db.session.query(Addon).filter_by(addon_id=addon_id).first()
            return addon
        except Exception as e:
            raise e
        
    @classmethod
    def create_addon(cls, addon_name, price, description):
        try:
            addon = Addon(addon_name=addon_name, price=price, description=description)
            db.session.add(addon)
            return addon
        except Exception as e:
            raise e    

    @classmethod
    def update_addon(cls, addon_id, addon_name=None, price=None, description=None, status=None):
        try:
            addon = db.session.query(Addon).filter_by(addon_id=addon_id).first()
            if addon_name:
                addon.addon_name = addon_name
            if price:
                addon.price = price
            if description:
                addon.description = description
            if status:
                addon.status = status
            return addon
        except Exception as e:
            raise e