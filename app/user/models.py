from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

class Role(db.Model):
    __tablename__ = 'role'

    role_id = Column(INTEGER, primary_key=True, unique=True)
    role = Column(String(45), nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    user_id = Column(INTEGER, primary_key=True, unique=True)
    role_id = Column(ForeignKey('role.role_id'), nullable=False, index=True)
    email = Column(String(255))
    password = Column(String(72), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    is_active = Column(INTEGER, server_default=text("1"))

    role = relationship('Role')

    # get user by email
    @classmethod
    def get_by_email(cls, email):
        try:
            user = db.session.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            raise e

    @classmethod
    def create_user(cls, email, password, first_name, last_name, role_id):
        try:
            user = User(email=email, password=password, first_name=first_name, last_name=last_name, role_id=role_id)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(cls, user_id):
        try:
            user = db.session.query(User).filter(User.user_id == user_id).first()
            return user
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls):
        try:
            users = db.session.query(User).all()
            return users
        except Exception as e:
            raise e
        
    @classmethod
    def update_user(cls, user_id, email, password, first_name, last_name, role_id):
        try:
            user = db.session.query(User).filter(User.user_id == user_id).first()
            user.email = email
            user.password = password
            user.first_name = first_name
            user.last_name = last_name
            user.role_id = role_id
            db.session.commit()
            return user
        except Exception as e:
            raise e
        
    @classmethod
    def deactivate_user(cls, user_id):
        try:
            user = db.session.query(User).filter(User.user_id == user_id).first()
            user.is_active = 0
            db.session.commit()
            return user
        except Exception as e:
            raise e
        
    @classmethod
    def activate_user(cls, user_id):
        try:
            user = db.session.query(User).filter(User.user_id == user_id).first()
            user.is_active = 1
            db.session.commit()
            return user
        except Exception as e:
            raise e
