from datetime import datetime
from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import Enum


#   `contract_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `purchase_id` INT UNSIGNED NOT NULL,
#   `vehicle_id` INT UNSIGNED NOT NULL,
#   `customer_id` INT UNSIGNED NOT NULL,
#   `finance_id` INT UNSIGNED NULL,
#   `customer_signature` VARCHAR(254) NULL,
#   `dealer_signature` VARCHAR(254) NULL,
#   `generated_date` DATETIME NULL DEFAULT NOW(),
#   `customer_signature_date` DATETIME NULL,
#   `dealer_signature_date` DATETIME NULL,
#   `dealer_signed` INT NOT NULL DEFAULT 0,
#   `customer_signed` INT NOT NULL DEFAULT 0,
#   `contract_path` VARCHAR(254) NULL,


class Contract(db.Model):
    __tablename__ = 'contract'


    class ContractStatus(Enum):
        ACTIVE = 1
        CUSTOMER_SIGNED = 2
        APPROVED = 3

    contract_id = Column(INTEGER(10, unsigned=True), primary_key=True)
    purchase_id = Column(ForeignKey('purchase.purchase_id'), nullable=False, unique=True)
    vehicle_id = Column(ForeignKey('vehicle.vehicle_id'), nullable=False)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False)
    finance_id = Column(ForeignKey('finance.finance_id'), nullable=True)
    customer_signature = Column(String(254), nullable=True)
    dealer_signature = Column(String(254), nullable=True)
    generated_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    customer_signature_date = Column(DateTime, nullable=True)
    dealer_signature_date = Column(DateTime, nullable=True)
    dealer_signed = Column(TINYINT(1), nullable=False, server_default=text("0"))
    customer_signed = Column(TINYINT(1), nullable=False, server_default=text("0"))
    contract_path = Column(String(254), nullable=True)

    finance = relationship('app.purchasing.models.Finance', backref='contracts', uselist=False)
    vehicle = relationship('app.inventory.models.Vehicle', backref='contracts', uselist=False)
    customer = relationship('app.customer.models.Customer', backref='contracts', uselist=False)


    @staticmethod
    def get_contract(contract_id):
        try:
            contract = db.session.query(Contract).filter_by(contract_id=contract_id).first()
            return contract
        except Exception as e:
            raise e
        
    @staticmethod
    def get_contract_by_purchase(purchase_id):
        try:
            contract = db.session.query(Contract).filter_by(purchase_id=purchase_id).first()
            return contract
        except Exception as e:
            raise e
        
    @staticmethod
    def create_contract(purchase_id, vehicle_id, customer_id, finance_id=None):
        try:
            contract = Contract(purchase_id=purchase_id, vehicle_id=vehicle_id, customer_id=customer_id, finance_id=finance_id)
            db.session.add(contract)
            db.session.commit()
            return contract
        except Exception as e:
            db.session.rollback()
            raise e
        
    def update_contract_signatures(contract_id, customer_signature=None, dealer_signature=None):
        try:
            contract = db.session.query(Contract).filter_by(contract_id=contract_id).first()
            if customer_signature:
                contract.customer_signature = customer_signature
                contract.customer_signature_date = datetime.now()
            if dealer_signature:
                contract.dealer_signature = dealer_signature
                contract.dealer_signature_date = datetime.now()
            return contract
        except Exception as e:
            raise e