from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship


class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = Column(INTEGER, primary_key=True, unique=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32))
    email = Column(String(254))
    password = Column(String(72), nullable=False)
    ssn = Column(String(11))
    birth_date = Column(Date)
    drivers_license = Column(String(16))
    address_id = Column(Integer)
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer, nullable=False)
    
    # serializer
    def serialize(self):
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'ssn': self.ssn,
            'birth_date': self.birth_date,
            'drivers_license': self.drivers_license,
            'address_id': self.address_id,
            'create_time': self.create_time,
            'status': self.status
        }
    
class CreditReport(db.Model):
    __tablename__ = 'credit_report'

    credit_report_id = Column(INTEGER, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    score = Column(INTEGER, nullable=False)

    customer = relationship('Customer')


class CustomerVehical(db.Model):
    __tablename__ = 'customer_vehical'

    customer_vehical_id = Column(INTEGER, primary_key=True, unique=True)
    vin = Column(String(45))
    year = Column(String(4))
    make = Column(String(254))
    model = Column(String(254))
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)

    customer = relationship('Customer')