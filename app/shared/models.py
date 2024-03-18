from app import db
# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(INTEGER, primary_key=True, unique=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32))
    email = Column(String(254))
    password = Column(String(32), nullable=False)
    ssn = Column(String(11))
    birth_date = Column(Date)
    drivers_license = Column(String(16))
    address_id = Column(Integer)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))