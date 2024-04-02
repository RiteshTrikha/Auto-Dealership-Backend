from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()
metadata = Base.metadata


class AppointmentDetail(Base):
    __tablename__ = 'appointment_details'

    appointment_details_id = Column(INTEGER, primary_key=True, unique=True)
    appointment_id = Column(ForeignKey('appointment.appointment_id'), nullable=False, index=True)
    customer_vehical_id = Column(ForeignKey('customer_vehical.customer_vehical_id'), nullable=False, index=True)
    customer_message = Column(String(512))
    notes = Column(String(512))

    appointment = relationship('Appointment')
    customer_vehical = relationship('CustomerVehical')

    #serialize
    def serialize(self):
        return {
            'appointment_details_id': self.appointment_details_id,
            'appointment_id': self.appointment_id,
            'customer_vehical_id': self.customer_vehical_id,
            'customer_message': self.customer_message,
            'notes': self.notes
        }
    
    @classmethod
    def get_all_appointment_details(cls):
        try:
            return db.session.query(AppointmentDetail).all()
        except Exception as e:
            raise e
    
    @classmethod
    def get_appointment_details_by_appointment_id(cls, appointment_id):
        try:
            return db.session.query(AppointmentDetail).filter_by(appointment_id=appointment_id).all()
        except Exception as e:
            raise e
        
    @classmethod
    def get_appointment_details_by_appointment_details_id(cls, appointment_details_id):
        try:
            return db.session.query(AppointmentDetail).filter_by(appointment_details_id=appointment_details_id).first()
        except Exception as e:
            raise e
    
    @classmethod
    def get_appointment_details_by_customer_vehical_id(cls, customer_vehical_id):
        try:
            return db.session.query(AppointmentDetail).filter_by(customer_vehical_id=customer_vehical_id).all()
        except Exception as e:
            raise e

    def create_appointment_details(self, appointment_id, customer_vehical_id, customer_message, notes):
        try:
            appointment_details = AppointmentDetail(appointment_id=appointment_id, customer_vehical_id=customer_vehical_id, customer_message=customer_message, notes=notes)
            db.session.add(appointment_details)
            db.session.commit()
            return appointment_details
        except Exception as e:
            raise e
    
    def update_appointment_details(self, appointment_details_id, appointment_id, customer_vehical_id, customer_message, notes):
        try:
            appointment_details = db.session.query(AppointmentDetail).filter_by(appointment_details_id=appointment_details_id).first()
            appointment_details.appointment_id = appointment_id
            appointment_details.customer_vehical_id = customer_vehical_id
            appointment_details.customer_message = customer_message
            appointment_details.notes = notes
            db.session.commit()
            return appointment_details
        except Exception as e:
            raise e

class Appointment(Base):
    __tablename__ = 'appointment'

    class appointmentType(Enum):
        SERVICE = 1
        TEST_DRIVE = 2

    class Status(Enum):
        CONFIRMED = 1
        CANCELLED = 2

    appointment_id = Column(INTEGER, primary_key=True, unique=True)
    time_slot_id = Column(ForeignKey('time_slot.time_slot_id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id'), index=True)
    appointment_type = Column(INTEGER, nullable=False)
    status = Column(INTEGER, nullable=False)

    customer = relationship('Customer')
    user = relationship('User')
    time_slot = relationship('TimeSlot')

    #serialize
    def serialize(self):
        return {
            'appointment_id': self.appointment_id,
            'time_slot_id': self.time_slot_id,
            'customer_id': self.customer_id,
            'user_id': self.user_id,
            'appointment_type': self.appointment_type,
            'status': self.status
        }
    
    @classmethod
    def get_all_appointments(cls):
        try:
            return db.session.query(Appointment).all()
        except Exception as e:
            raise e
    
    @classmethod
    def get_appointment_by_id(cls, appointment_id):
        try:
            return db.session.query(Appointment).filter_by(appointment_id=appointment_id).first()
        except Exception as e:
            raise e
    
    @classmethod
    def get_appointments_by_user_id(cls, user_id):
        try:
            return db.session.query(Appointment).filter_by(user_id=user_id).all()
        except Exception as e:
            raise e
    
    @classmethod
    def get_appointments_by_customer_id(cls, customer_id):
        try:
            return db.session.query(Appointment).filter_by(customer_id=customer_id).all()
        except Exception as e:
            raise e
    
    @classmethod
    def get_all_appointments_by_customer_id_and_appointment_type(cls, customer_id, appointment_type):
        try:
            return db.session.query(Appointment).filter_by(customer_id=customer_id, appointment_type=appointment_type).all()
        except Exception as e:
            raise e
    
    @classmethod
    def get_all_appointments_by_appointment_type(cls, appointment_type):
        try:
            return db.session.query(Appointment).filter_by(appointment_type=appointment_type).all()
        except Exception as e:
            raise e

    @classmethod
    def get_appointments_by_time_slot_id(cls, time_slot_id):
        try:
            return db.session.query(Appointment).filter_by(time_slot_id=time_slot_id).all()
        except Exception as e:
            raise e

    #(maybe add cancel by user or customer)
    @classmethod
    def cancel_appointment(self, appointment_id):
        try:
            appointment = db.session.query(Appointment).filter_by(appointment_id=appointment_id).first()
            appointment.status = 2
            db.session.commit()
            return appointment
        except Exception as e:
            raise e
    
    def create_appointment(self, time_slot_id, customer_id, user_id, appointment_type, status):
        try:
            appointment = Appointment(time_slot_id=time_slot_id, customer_id=customer_id, user_id=user_id, appointment_type=appointment_type, status=status)
            db.session.add(appointment)
            db.session.commit()
            return appointment
        except Exception as e:
            raise e
    
    def update_appointment(self, appointment_id, time_slot_id, customer_id, user_id, appointment_type, status):
        try:
            appointment = db.session.query(Appointment).filter_by(appointment_id=appointment_id).first()
            appointment.time_slot_id = time_slot_id
            appointment.customer_id = customer_id
            appointment.user_id = user_id
            appointment.appointment_type = appointment_type
            appointment.status = status
            db.session.commit()
            return appointment  
        except Exception as e:
            raise e


class TimeSlot(Base):
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

    role = relationship('Role')

    #serialize
    def serialize(self):
        return {
            'time_slot_id': self.time_slot_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'time_slot_type': self.time_slot_type,
            'is_available': self.is_available
        }
    
    @classmethod
    def get_all_time_slots(cls):
        try:
            return db.session.query(TimeSlot).all()
        except Exception as e:
            raise e

    @classmethod
    def get_available_time_slots(cls):
        try:
            return db.session.query(TimeSlot).filter_by(is_available=1).all()
        except Exception as e:
            raise e
    
    @classmethod
    def get_time_slots_by_type(cls, time_slot_type):
        try:
            return db.session.query(TimeSlot).filter_by(time_slot_type=time_slot_type).all()
        except Exception as e:
            raise e
    
    @classmethod
    def get_time_slot_by_id(cls, time_slot_id):
        try:
            return db.session.query(TimeSlot).filter_by(time_slot_id=time_slot_id).first()
        except Exception as e:
            raise e

    def create_time_slot(self, start_time, end_time, time_slot_type, is_available):
        try:
            time_slot = TimeSlot(start_time=start_time, end_time=end_time, time_slot_type=time_slot_type, is_available=is_available)
            db.session.add(time_slot)
            db.session.commit()
            return time_slot
        except Exception as e:
            raise e
    
    def update_time_slot(self, time_slot_id, start_time, end_time, time_slot_type, is_available):
        try:
            time_slot = db.session.query(TimeSlot).filter_by(time_slot_id=time_slot_id).first()
            time_slot.start_time = start_time
            time_slot.end_time = end_time
            time_slot.time_slot_type = time_slot_type
            time_slot.is_available = is_available
            db.session.commit()
            return time_slot
        except Exception as e:
            raise e