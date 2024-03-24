from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'

    user_id = Column(INTEGER, primary_key=True, unique=True)
    role_id = Column(ForeignKey('role.role_id'), nullable=False, index=True)
    email = Column(String(255))
    password = Column(String(72), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    role = relationship('Role')

    #serialize
    def serialize(self):
        return {
            'user_id': self.user_id,
            'role_id': self.role_id,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'create_time': self.create_time
        }