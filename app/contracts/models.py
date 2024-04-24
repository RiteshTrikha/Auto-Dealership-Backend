from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import Enum


#CREATE TABLE IF NOT EXISTS `DealershipDB`.`contract` (
#  `contract_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#  `purchase_id` INT UNSIGNED NOT NULL,
#  `contract_type` INT NULL,
#  `contract_status` INT NULL,
#  `contract_date` DATETIME NULL DEFAULT NOW(),
#  `contract_path` VARCHAR(254) NULL,


class Contract(db.Model):
    __tablename__ = 'contract'
    __table_args__ = (db.UniqueConstraint('purchase_id', 'contract_type', name='purchase_contract_type_uc'),)

    class ContractType(Enum):
        PURCHASE = 1
        FINANCE = 2

    class ContractStatus(Enum):
        ACTIVE = 1
        CUSTOMER_SIGNED = 2
        APPROVED = 3

    contract_id = Column(INTEGER(unsigned=True), primary_key=True)
    purchase_id = Column(ForeignKey('purchase.purchase_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    contract_type = Column(INTEGER)
    contract_status = Column(INTEGER)
    signer_full_name = Column(String(45))
    customer_signature = Column(String(254))
    dealer_signature = Column(String(254))
    vehicle_year = Column(String(4))
    vehicle_make = Column(String(45))
    vehicle_model = Column(String(45))
    vehicle_vin = Column(String(17))
    contract_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    contract_path = Column(String(254))

    @staticmethod
    def get_contract(contract_id):
        try:
            contract = db.session.query(Contract).filter_by(contract_id=contract_id).first()
            return contract
        except Exception as e:
            raise e
        
    @staticmethod
    def create_contract(purchase_id, contract_type, contract_path, signer_full_name, vehicle_year, vehicle_make, vehicle_model, vehicle_vin):
        try:
            contract = Contract(purchase_id=purchase_id, contract_type=contract_type, 
                                contract_path=contract_path, signer_full_name=signer_full_name, 
                                vehicle_year=vehicle_year, vehicle_make=vehicle_make, 
                                vehicle_model=vehicle_model, vehicle_vin=vehicle_vin,
                                contract_status=Contract.ContractStatus.ACTIVE.value)
            db.session.add(contract)
            return contract
        except Exception as e:
            raise e
        
    def update_contract_signatures(contract_id, customer_signature=None, dealer_signature=None):
        try:
            contract = db.session.query(Contract).filter_by(contract_id=contract_id).first()
            if customer_signature:
                contract.customer_signature = customer_signature
            if dealer_signature:
                contract.dealer_signature = dealer_signature
            return contract
        except Exception as e:
            raise e
        
    @staticmethod
    def update_contract_status(contract_id, status):
        try:
            contract = db.session.query(Contract).filter_by(contract_id=contract_id).first()
            contract.contract_status = status
            return contract
        except Exception as e:
            raise e