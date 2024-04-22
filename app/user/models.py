from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

class Role(db.Model):
    __tablename__ = 'role'

    role_id = Column(INTEGER, primary_key=True, unique=True)
    role = Column(INTEGER, nullable=False)

    #get role by role_id
    @classmethod
    def get_role_by_role_id(cls, role_id):
        try:
            return db.session.query(Role).filter(Role.role_id == role_id).first()
        except Exception as e:
            raise e
        
    #get all roles
    @classmethod
    def get_all_roles(cls):
        try:
            return db.session.query(Role).all()
        except Exception as e:
            raise e


class User(db.Model):
    __tablename__ = 'user'

    user_id = Column(INTEGER, primary_key=True, unique=True)
    role_id = Column(ForeignKey('role.role_id'), nullable=False, index=True)
    email = Column(String(255))
    password = Column(String(72), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    role = relationship('Role', backref='user')

    #create user
    @classmethod
    def create(cls, role_id, email, password, first_name, last_name):
        try:
            user = User(role_id=role_id, email=email, password=password, first_name=first_name, last_name=last_name)
            db.session.add(user)
            return user.user_id
        except Exception as e:
            raise e

    #get user by user_id
    @classmethod
    def get_user_by_user_id(cls, user_id):
        try:
            return db.session.query(User).filter(User.user_id == user_id).first()
        except Exception as e:
            raise e

    #get all users by user_id
    @classmethod
    def get_all_users(cls):
        try:
            return db.session.query(User).all()
        except Exception as e:
            raise e

    #get by role_id
    @classmethod
    def get_by_role_id(cls, role_id):
        try:
            return db.session.query(User).filter(User.role_id == role_id).all()
        except Exception as e:
            raise e    
