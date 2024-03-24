# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class RetailItem(Base):
    __tablename__ = 'retail_item'

    retail_item_id = Column(INTEGER, primary_key=True, unique=True)
    name = Column(String(45))
    price = Column(Integer)
    description = Column(String(254))


class Role(Base):
    __tablename__ = 'role'

    role_id = Column(INTEGER, primary_key=True, unique=True)
    role = Column(INTEGER, nullable=False)


class Vehical(Base):
    __tablename__ = 'vehical'

    vehical_id = Column(INTEGER, primary_key=True, unique=True)
    vin = Column(String(17), nullable=False)
    price = Column(Integer)
    year = Column(String(4))
    make = Column(String(45))
    model = Column(String(45))
    miles = Column(Integer)
    mpg = Column(Integer)
    fuel_type = Column(String(45))
    transmission = Column(String(45))
    vehical_status = Column(Integer)


class CreditReport(Base):
    __tablename__ = 'credit_report'

    credit_report_id = Column(INTEGER, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    score = Column(Integer, nullable=False)

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


class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(INTEGER, primary_key=True, unique=True)
    role_id = Column(ForeignKey('role.role_id'), nullable=False, index=True)
    email = Column(String(255))
    password = Column(String(32), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    role = relationship('Role')


class Negotiation(Base):
    __tablename__ = 'negotiation'

    negotiation_id = Column(INTEGER, primary_key=True, unique=True)
    vehical_id = Column(ForeignKey('vehical.vehical_id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    negotiation_status = Column(String(45), nullable=False, server_default=text("'Active'"))
    start_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    end_date = Column(DateTime)

    customer = relationship('Customer')
    vehical = relationship('Vehical')


class Purchase(Base):
    __tablename__ = 'purchase'

    purchase_id = Column(INTEGER, primary_key=True, unique=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    purchase_date = Column(DateTime)
    purchase_type = Column(String(45))
    payment_method = Column(String(45))
    sub_total = Column(Integer)
    tax = Column(Float)
    total = Column(Integer)

    customer = relationship('Customer')





class Log(Base):
    __tablename__ = 'Log'

    log_id = Column(INTEGER, primary_key=True, unique=True)
    type = Column(String(45))
    message = Column(String(512))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    customer_id = Column(ForeignKey('customer.customer_id'), index=True)
    employee_id = Column(ForeignKey('employee.employee_id'), index=True)

    customer = relationship('Customer')
    employee = relationship('Employee')





class Finance(Base):
    __tablename__ = 'finance'

    finance_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(ForeignKey('purchase.purchase_id'), nullable=False, unique=True)
    apy = Column(Float)
    term = Column(Integer)
    paid = Column(Integer)
    finance_status = Column(Integer)

    purchase = relationship('Purchase')


class Offer(Base):
    __tablename__ = 'offer'

    offer_id = Column(INTEGER, primary_key=True, unique=True)
    negotiation_id = Column(ForeignKey('negotiation.negotiation_id'), nullable=False, index=True)
    offer_price = Column(Integer, nullable=False)
    offer_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    offer_status = Column(String(45))

    negotiation = relationship('Negotiation')


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
    price = Column(Integer)

    purchase = relationship('Purchase')





class CounterOffer(Base):
    __tablename__ = 'counter_offer'

    counter_offer_id = Column(INTEGER, primary_key=True, unique=True)
    offer_id = Column(ForeignKey('offer.offer_id'), nullable=False, unique=True)
    counter_price = Column(Integer, nullable=False)
    counter_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    counter_status = Column(String(45))

    offer = relationship('Offer')
