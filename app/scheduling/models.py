from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import Enum

class Appointment(db.Model):
    __tablename__ = 'appointment'

    class appointmentType(Enum):
        SERVICE = 1
        TEST_DRIVE = 2

    class Status(Enum):
        CONFIRMED = 1
        CANCELLED = 2
        PENDING = 3

    appointment_id = Column(INTEGER, primary_key=True, unique=True)
    time_slot_id = Column(ForeignKey('time_slot.time_slot_id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    appointment_type = Column(INTEGER, nullable=False)
    status = Column(INTEGER, nullable=False, server_default=text("3"))

    customer = relationship('app.customer.models.Customer', backref='appointment')
   # user = relationship('app.user.models.User', backref='appointment')
    time_slot = relationship('TimeSlot' , backref='appointment')
    
    #get test drive appointments by customer id
    @classmethod
    def get_test_drive_appointments_by_customer_id(cls, customer_id):
        try:
            return db.session.query(Appointment).filter(Appointment.customer_id == customer_id, Appointment.appointment_type == 2).all()
        except Exception as e:
            raise e
        
    #get service appointments by customer id
    @classmethod
    def get_service_appointments_by_customer_id(cls, customer_id):
        try:
            return db.session.query(Appointment).filter(Appointment.customer_id == customer_id, Appointment.appointment_type == 1).all()
        except Exception as e:
            raise e
        
    #get all appointments by customer id
    @classmethod
    def get_all_appointments_by_customer_id(cls, customer_id):
        try:
            return db.session.query(Appointment).filter(Appointment.customer_id == customer_id).all()
        except Exception as e:
            raise e

    #get all test drive appointments
    @classmethod
    def get_test_drive_appointments(cls):
        try:
            return db.session.query(Appointment).filter(Appointment.appointment_type == 2).all()
        except Exception as e:
            raise e
        
    #get all service appointments
    @classmethod
    def get_service_appointments(cls):
        try:
            return db.session.query(Appointment).filter(Appointment.appointment_type == 1).all()
        except Exception as e:
            raise e

    #get appointment by appointment id
    @classmethod
    def get_appointment_by_appointment_id(cls, appointment_id):
        try:
            return db.session.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
        except Exception as e:
            raise e

    #get all appointments
    @classmethod
    def get_all_appointments(cls):
        try:
            return db.session.query(Appointment).all()
        except Exception as e:
            raise e

    #create appointment    
    @classmethod
    def create_appointment(self, time_slot_id, customer_id, appointment_type, status):
        try:
            appointment = Appointment(time_slot_id=time_slot_id, customer_id=customer_id, appointment_type=appointment_type, status=status)
            db.session.add(appointment)
            return appointment
        except Exception as e:
            raise e
    
    #update appointment status
    @classmethod
    def update_appointment_status(self, appointment_id, status):
        try:
            appointment = db.session.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
            appointment.status = status
            return appointment
        except Exception as e:
            raise e



class TimeSlot(db.Model):
    __tablename__ = 'time_slot'

    class TimeSlotType(Enum):
        SERVICE = 1
        TEST_DRIVE = 2

    class isAvailable(Enum):
        AVAILABLE = 1
        NOT_AVAILABLE = 0

    time_slot_id = Column(INTEGER, primary_key=True, unique=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    time_slot_type = Column(Integer, nullable=False)
    is_available = Column(Integer, nullable=False)

    #role = relationship('Role')

    #get test drive time slots
    @classmethod
    def get_test_drive_time_slots(cls):
        try:
            return db.session.query(TimeSlot).filter(TimeSlot.time_slot_type == 2).all()
        except Exception as e:
            raise e
        
    #get service time slots
    @classmethod
    def get_service_time_slots(cls):
        try:
            return db.session.query(TimeSlot).filter(TimeSlot.time_slot_type == 1).all()
        except Exception as e:
            raise e

    #get all time slots 
    @classmethod
    def get_all_time_slots(cls):
        try:
            return db.session.query(TimeSlot).all()
        except Exception as e:
            raise 
        
    #get all available time slots
    @classmethod
    def get_available_time_slots(cls):
        try:
            return db.session.query(TimeSlot).filter(TimeSlot.is_available == 1).all()
        except Exception as e:
            raise e
        
    #get all time slots by time slot id
    @classmethod
    def get_time_slot_by_time_slot_id(cls, time_slot_id):
        try:
            return db.session.query(TimeSlot).filter(TimeSlot.time_slot_id == time_slot_id).first()
        except Exception as e:
            raise e
        
    #check if time slot is available
    @classmethod
    def is_time_slot_available(cls, time_slot_id):
        try:
            time_slot = db.session.query(TimeSlot).filter(TimeSlot.time_slot_id == time_slot_id).first()
            return time_slot.is_available
        except Exception as e:
            raise e
    
    #create time slot     
    @classmethod
    def create_time_slot(self, start_time, end_time, time_slot_type, is_available):
        try:
            time_slot = TimeSlot(start_time=start_time, end_time=end_time, time_slot_type=time_slot_type, is_available=is_available)
            db.session.add(time_slot)
            return time_slot
        except Exception as e:
            raise e
        
    #update time slot availability
    @classmethod
    def update_time_slot_availability(self, time_slot_id, is_available):
        try:
            time_slot = db.session.query(TimeSlot).filter(TimeSlot.time_slot_id == time_slot_id).first()
            time_slot.is_available = is_available
            return time_slot
        except Exception as e:
            raise e        



class Service_Ticket(db.Model):
    __tablename__ = 'service_ticket'

    class Status(Enum):
        OPEN = 1
        CLOSED = 2 
        CANCELLED = 3

    service_ticket_id = Column(INTEGER, primary_key=True, unique=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, index=True)
    customer_vehical_id = Column(ForeignKey('customer_vehical.customer_vehical_id'), nullable=False, index=True)
    time_slot_id = Column(ForeignKey('time_slot.time_slot_id'), nullable=False, index=True)
    customer_notes = Column(String(255))
    technician_notes = Column(String(255))
    status = Column(INTEGER, nullable=False)

    customer = relationship('app.customer.models.Customer' , backref='service_ticket')
    vehical = relationship('app.customer.models.CustomerVehical' , backref='service_ticket')
    user = relationship('app.user.models.User' , backref='service_ticket')
    time_slot = relationship('app.scheduling.models.TimeSlot' , backref='service_ticket')
    services = relationship('Service_Ticket_Service', backref='service_ticket', overlaps='service_ticket')

    
    #get service ticket by service ticket id
    @classmethod
    def get_service_ticket_by_service_ticket_id(cls, service_ticket_id):
        try:
            return db.session.query(Service_Ticket).filter(Service_Ticket.service_ticket_id == service_ticket_id).first()
        except Exception as e:
            raise e

    #get all service tickets by customer id
    @classmethod
    def get_all_service_tickets_by_customer_id(cls, customer_id):
        try:
            return db.session.query(Service_Ticket).filter(Service_Ticket.customer_id == customer_id).all()
        except Exception as e:
            raise e
        
    #get all service tickets by user id
    @classmethod
    def get_all_service_tickets_by_user_id(cls, user_id):
        try:
            return db.session.query(Service_Ticket).filter(Service_Ticket.user_id == user_id).all()
        except Exception as e:
            raise e
        
    #get all service tickets by customer vehical id
    @classmethod
    def get_all_service_tickets_by_customer_vehical_id(cls, customer_vehical_id):
        try:
            return db.session.query(Service_Ticket).filter(Service_Ticket.customer_vehical_id == customer_vehical_id).all()
        except Exception as e:
            raise e
        
    #get all service tickets by time slot id
    @classmethod
    def get_all_service_tickets_by_time_slot_id(cls, time_slot_id):
        try:
            return db.session.query(Service_Ticket).filter(Service_Ticket.time_slot_id == time_slot_id).all()
        except Exception as e:
            raise e

    #get all service tickets
    @classmethod
    def get_all_service_tickets(cls):
        try:
            return db.session.query(Service_Ticket).all()
        except Exception as e:
            raise e

    #create service ticket
    @classmethod
    def create_service_ticket(self, customer_id, user_id, customer_vehical_id, time_slot_id, customer_notes, technician_notes, status):
        try:
            service_ticket = Service_Ticket(customer_id=customer_id, user_id=user_id, customer_vehical_id=customer_vehical_id, time_slot_id=time_slot_id, customer_notes=customer_notes, technician_notes=technician_notes, status=status)
            db.session.add(service_ticket)
            return service_ticket
        except Exception as e:
            raise e
        
    #add technician notes to service ticket
    @classmethod
    def add_technician_notes_to_service_ticket(self, service_ticket_id, technician_notes):
        try:
            service_ticket = db.session.query(Service_Ticket).filter(Service_Ticket.service_ticket_id == service_ticket_id).first()
            service_ticket.technician_notes = technician_notes
            return service_ticket
        except Exception as e:
            raise e
        
    #add customer notes to service ticket
    @classmethod
    def add_customer_notes_to_service_ticket(self, service_ticket_id, customer_notes):
        try:
            service_ticket = db.session.query(Service_Ticket).filter(Service_Ticket.service_ticket_id == service_ticket_id).first()
            service_ticket.customer_notes = customer_notes
            return service_ticket
        except Exception as e:
            raise e
        
    #update service ticket status
    @classmethod
    def update_service_ticket_status(self, service_ticket_id, status):
        try:
            service_ticket = db.session.query(Service_Ticket).filter(Service_Ticket.service_ticket_id == service_ticket_id).first()
            service_ticket.status = status
            return service_ticket
        except Exception as e:
            raise e


class Service(db.Model):
    __tablename__ = 'service'

    service_id = Column(INTEGER, primary_key=True, unique=True)
    service_type = Column(String(255), nullable=False)
    price = Column(INTEGER, nullable=False)
    description = Column(String(255), nullable=False)
    
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

    #update service
    @classmethod
    def update_service(self, service_id, service_type, price, description):
        try:
            service = db.session.query(Service).filter(Service.service_id == service_id).first()
            service.service_type = service_type
            service.price = price
            service.description = description
            return service
        except Exception as e:
            raise e


class Service_Ticket_Service(db.Model):
    __tablename__ = 'service_ticket_service'

    service_ticket_id = Column(ForeignKey('service_ticket.service_ticket_id'), primary_key=True, nullable=False)
    service_id = Column(ForeignKey('service.service_id'), primary_key=True, nullable=False)

    service = relationship('Service', backref='service_ticket_services')
    ticket = relationship('Service_Ticket', backref='service_ticket_services', overlaps='services')

    
    #get all services by service ticket id
    @classmethod
    def get_all_services_by_service_ticket_id(cls, service_ticket_id):
        try:
            return db.session.query(Service_Ticket_Service).filter(Service_Ticket_Service.service_ticket_id == service_ticket_id).all()
        except Exception as e:
            raise e
    
    #get all service tickets by service id
    @classmethod
    def get_all_service_tickets_by_service_id(cls, service_id):
        try:
            return db.session.query(Service_Ticket_Service).filter(Service_Ticket_Service.service_id == service_id).all()
        except Exception as e:
            raise e
    
    #get all service ticket services
    @classmethod
    def get_all_service_ticket_services(cls):
        try:
            return db.session.query(Service_Ticket_Service).all()
        except Exception as e:
            raise e
        
    #create service ticket service
    @classmethod
    def create_service_ticket_service(self, service_ticket_id, service_id):
        try:
            service_ticket_service = Service_Ticket_Service(service_ticket_id=service_ticket_id, service_id=service_id)
            db.session.add(service_ticket_service)
            return service_ticket_service
        except Exception as e:
            raise e

    #update service ticket service
    @classmethod
    def update_service_ticket_service(self, service_ticket_id, service_id):
        try:
            service_ticket_service = db.session.query(Service_Ticket_Service).filter(Service_Ticket_Service.service_ticket_id == service_ticket_id, Service_Ticket_Service.service_id == service_id).first()
            return service_ticket_service
        except Exception as e:
            raise e