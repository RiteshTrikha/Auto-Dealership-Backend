# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, INTEGER, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class RetailItem(Base):
    __tablename__ = 'retail_item'

    retail_item_id = Column(INTEGER, primary_key=True, unique=True)
    name = Column(String(45))
    price = Column(INTEGER)
    description = Column(String(254))


class Role(Base):
    __tablename__ = 'role'

    role_id = Column(INTEGER, primary_key=True, unique=True)
    role = Column(INTEGER, nullable=False)


class Vehical(Base):
    __tablename__ = 'vehical'

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
    vehical_status = Column(INTEGER)


class CreditReport(Base):
    __tablename__ = 'credit_report'

    credit_report_id = Column(INTEGER, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    score = Column(INTEGER, nullable=False)

    customer = relationship('Customer')


class CustomerVehical(Base):
    __tablename__ = 'customer_vehical'

    customer_vehical_id = Column(INTEGER, primary_key=True, unique=True)
    vin = Column(String(45))
    year = Column(String(4))
    make = Column(String(254))
    model = Column(String(254))
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)

    customer = relationship('Customer')


class user(Base):
    __tablename__ = 'user'

    user_id = Column(INTEGER, primary_key=True, unique=True)
    role_id = Column(ForeignKey('role.role_id'), nullable=False, index=True)
    email = Column(String(255))
    password = Column(String(72), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    role = relationship('Role')


class Purchase(Base):
    __tablename__ = 'purchase'

    purchase_id = Column(INTEGER, primary_key=True, unique=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    purchase_date = Column(DateTime)
    purchase_type = Column(INTEGER)
    payment_method = Column(INTEGER)
    sub_total = Column(INTEGER)
    tax = Column(Float)
    total = Column(INTEGER)

    customer = relationship('Customer')


class TimeSlot(Base):
    __tablename__ = 'time_slot'

    time_slot_id = Column(INTEGER, primary_key=True, unique=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    role_id = Column(ForeignKey('role.role_id'), nullable=False, index=True)
    is_available = Column(INTEGER, nullable=False)

    role = relationship('Role')


class Log(Base):
    __tablename__ = 'Log'

    log_id = Column(INTEGER, primary_key=True, unique=True)
    type = Column(String(45))
    message = Column(String(512))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    customer_id = Column(ForeignKey('customer.customer_id'), index=True)
    user_id = Column(ForeignKey('user.user_id'), index=True)

    customer = relationship('Customer')
    user = relationship('user')


class Finance(Base):
    __tablename__ = 'finance'

    finance_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(ForeignKey('purchase.purchase_id'), nullable=False, unique=True)
    apy = Column(Float)
    term = Column(INTEGER)
    paid = Column(INTEGER)
    finance_status = Column(INTEGER)

    purchase = relationship('Purchase')


class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(ForeignKey('purchase.purchase_id'), nullable=False, index=True)
    ccv = Column(String(45))
    expiration = Column(String(45))
    card_number = Column(String(45))
    routing_number = Column(String(45))
    account_number = Column(String(45))

    purchase = relationship('Purchase')


class PurchaseItem(Base):
    __tablename__ = 'purchase_item'

    purchase_item_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(ForeignKey('purchase.purchase_id'), nullable=False, unique=True)
    item_id = Column(INTEGER, nullable=False, unique=True)
    price = Column(INTEGER)

    purchase = relationship('Purchase')


class Appointment(Base):
    __tablename__ = 'appointment'

    appointment_id = Column(INTEGER, primary_key=True, unique=True)
    time_slot_id = Column(ForeignKey('time_slot.time_slot_id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.user_id'), index=True)
    appointment_type = Column(INTEGER, nullable=False)
    status = Column(INTEGER, nullable=False)

    customer = relationship('Customer')
    user = relationship('user')
    time_slot = relationship('TimeSlot')

    # functions
    def serialize(self):
        return {
            'appointment_id': self.appointment_id,
            'time_slot_id': self.time_slot_id,
            'customer_id': self.customer_id,
            'user_id': self.user_id,
            'appointment_type': self.appointment_type,
            'status': self.status
        }


class AppointmentDetail(Base):
    __tablename__ = 'appointment_details'

    appointment_details_id = Column(INTEGER, primary_key=True, unique=True)
    appointment_id = Column(ForeignKey('appointment.appointment_id'), nullable=False, index=True)
    customer_vehical_id = Column(ForeignKey('customer_vehical.customer_vehical_id'), nullable=False, index=True)
    customer_message = Column(String(512))
    notes = Column(String(512))

    appointment = relationship('Appointment')
    customer_vehical = relationship('CustomerVehical')
