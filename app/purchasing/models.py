from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import Enum

# `purchase` (
#   `purchase_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `customer_id` INT UNSIGNED NOT NULL,
#   `open_date` DATETIME NULL DEFAULT NOW(),
#   `close_date` DATETIME NULL,
#   `purchase_final_date` DATETIME NULL,
#   `purchase_type` INT NULL,
#   `tax` FLOAT NULL,

# `finance` (
#   `finance_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `purchase_id` INT UNSIGNED NOT NULL,
#   `start_date` DATETIME NULL DEFAULT NOW(),
#   `end_date` DATETIME NULL,
#   `down_payment` INT NULL,
#   `loan_amount` INT NULL,
#   `apy` FLOAT NULL,
#   `term` INT NULL,
#   `paid` INT NULL,
#   `finance_status` INT NULL,

# `payment` (
#   `payment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `purchase_id` INT UNSIGNED NOT NULL,
#   `finance_id` INT UNSIGNED NULL,
#   `routing_number` VARCHAR(45) NULL,
#   `account_number` VARCHAR(45) NULL,
#   `payment_amount` INT NULL,

# `purchase_item` (
#   `purchase_service_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `purchase_id` INT UNSIGNED NOT NULL,
#   `service_id` INT UNSIGNED NOT NULL,

# `purchase_vehical` (
#   `purchase_vehical_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `purchase_id` INT UNSIGNED NOT NULL,
#   `vehical_id` INT UNSIGNED NOT NULL,


class Purchase(db.Model):
    __tablename__ = 'purchase'

    class PurchaseType(Enum):
        ACH = 0
        FINANCE = 1

    purchase_id = Column(INTEGER, primary_key=True, unique=True)
    customer_id = Column(INTEGER, ForeignKey('customer.customer_id'))
    open_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    close_date = Column(DateTime)
    purchase_final_date = Column(DateTime)
    purchase_type = Column(INTEGER)
    tax = Column(Float)

    customer = relationship('Customer', back_populates='purchase')
    finance = relationship('Finance', back_populates='purchase')
    payment = relationship('Payment', back_populates='purchase')
    purchase_item = relationship('PurchaseItem', back_populates='purchase')
    purchase_vehical = relationship('PurchaseVehical', back_populates='purchase')

    @classmethod
    def get_purchases(cls):
        try:
            purchases = db.session.query(Purchase).all()
            return purchases
        except Exception as e:
            raise e

    @classmethod
    def get_purchase(cls, purchase_id):
        try:
            purchase = db.session.query(Purchase).filter_by(purchase_id=purchase_id).first()
            return purchase
        except Exception as e:
            raise e

    @classmethod
    def create_purchase(cls, customer_id, purchase_type, payment_method, tax):
        try:
            purchase = Purchase(customer_id=customer_id, purchase_type=purchase_type, 
                                payment_method=payment_method, tax=tax)
            db.session.add(purchase)
            return purchase
        except Exception as e:
            raise e

    @classmethod
    def update_purchase(cls, purchase_id, customer_id=None, purchase_type=None, 
                        payment_method=None, tax=None):
        try:
            purchase = db.session.query(Purchase).filter_by(purchase_id=purchase_id).first()
            if customer_id:
                purchase.customer_id = customer_id
            if purchase_type:
                purchase.purchase_type = purchase_type
            if payment_method:
                purchase.payment_method = payment_method
            if tax:
                purchase.tax = tax
            return purchase.purchase_id
        except Exception as e:
            raise e

    @classmethod
    def update_purchase_status(cls, purchase_id, status):
        try:
            purchase = db.session.query(Purchase).filter_by(purchase_id=purchase_id).first()
            purchase.status = status
            return purchase
        except Exception as e:
            raise e

class Finance(db.Model):
    __tablename__ = 'finance'

    class FinanceStatus(Enum):
        ACTIVE = 0
        PAID = 1

    finance_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(INTEGER, ForeignKey('purchase.purchase_id'))
    start_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    end_date = Column(DateTime)
    down_payment = Column(INTEGER)
    loan_amount = Column(INTEGER)
    apy = Column(Float)
    term = Column(INTEGER)
    paid = Column(INTEGER)
    finance_status = Column(INTEGER)

    payment = relationship('Payment', back_populates='finance')

    @classmethod
    def get_finances(cls):
        try:
            finances = db.session.query(Finance).all()
            return finances
        except Exception as e:
            raise e

    @classmethod
    def get_finance(cls, finance_id):
        try:
            finance = db.session.query(Finance).filter_by(finance_id=finance_id).first()
            return finance
        except Exception as e:
            raise e

    @classmethod
    def create_finance(cls, purchase_id, start_date, end_date, down_payment, loan_amount, apy, 
                       term, paid, finance_status):
        try:
            finance = Finance(purchase_id=purchase_id, start_date=start_date, 
                              end_date=end_date, down_payment=down_payment, 
                              loan_amount=loan_amount, apy=apy, term=term, 
                              paid=paid, finance_status=finance_status)
            db.session.add(finance)
            return finance.finance_id
        except Exception as e:
            raise e

    @classmethod
    def update_finance(cls, finance_id, purchase_id=None, start_date=None, end_date=None, 
                       down_payment=None, loan_amount=None, apy=None, term=None, paid=None):
        try:
            finance = db.session.query(Finance).filter_by(finance_id=finance_id).first()
            if purchase_id:
                finance.purchase_id = purchase_id
            if start_date:
                finance.start_date = start_date
            if end_date:
                finance.end_date = end_date
            if down_payment:
                finance.down_payment = down_payment
            if loan_amount:
                finance.loan_amount = loan_amount
            if apy:
                finance.apy = apy
            if term:
                finance.term = term
            if paid:
                finance.paid = paid
            return finance.finance_id
        except Exception as e:
            raise e

    @classmethod
    def update_finance_status(cls, finance_id, status):
        try:
            finance = db.session.query(Finance).filter_by(finance_id=finance_id).first()
            finance.status = status
            return finance
        except Exception as e:
            raise e
            
class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(INTEGER, ForeignKey('purchase.purchase_id'))
    finance_id = Column(INTEGER, ForeignKey('finance.finance_id'))
    routing_number = Column(String(45))
    account_number = Column(String(45))
    payment_amount = Column(INTEGER)

    @classmethod
    def get_payments(cls):
        try:
            payments = db.session.query(Payment).all()
            return payments
        except Exception as e:
            raise e

    @classmethod
    def get_payment(cls, payment_id):
        try:
            payment = db.session.query(Payment).filter_by(payment_id=payment_id).first()
            return payment
        except Exception as e:
            raise e

    @classmethod
    def create_payment(cls, purchase_id, finance_id, routing_number, account_number, payment_amount):
        try:
            payment = Payment(purchase_id=purchase_id, finance_id=finance_id, 
                              routing_number=routing_number, account_number=account_number, 
                              payment_amount=payment_amount)
            db.session.add(payment)
            return payment.payment_id
        except Exception as e:
            raise e

    @classmethod
    def update_payment(cls, payment_id, purchase_id=None, finance_id=None, routing_number=None, 
                       account_number=None, payment_amount=None):
        try:
            payment = db.session.query(Payment).filter_by(payment_id=payment_id).first()
            if purchase_id:
                payment.purchase_id = purchase_id
            if finance_id:
                payment.finance_id = finance_id
            if routing_number:
                payment.routing_number = routing_number
            if account_number:
                payment.account_number = account_number
            if payment_amount:
                payment.payment_amount = payment_amount
            return payment.payment_id
        except Exception as e:
            raise e
        
class PurchaseItem(db.Model):
    __tablename__ = 'purchase_item'

    purchase_item_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(INTEGER, ForeignKey('purchase.purchase_id'))
    service_id = Column(INTEGER, ForeignKey('service.service_id'))

    service = relationship('Service', back_populates='purchase_item')

    @classmethod
    def get_purchase_items(cls):
        try:
            purchase_items = db.session.query(PurchaseItem).all()
            return purchase_items
        except Exception as e:
            raise e

    @classmethod
    def get_purchase_item(cls, purchase_item_id):
        try:
            purchase_item = db.session.query(PurchaseItem).filter_by(purchase_item_id=purchase_item_id).first()
            return purchase_item
        except Exception as e:
            raise e

    @classmethod
    def create_purchase_item(cls, purchase_id, service_id):
        try:
            purchase_item = PurchaseItem(purchase_id=purchase_id, service_id=service_id)
            db.session.add(purchase_item)
            return purchase_item.purchase_item_id
        except Exception as e:
            raise e

    @classmethod
    def update_purchase_item(cls, purchase_item_id, purchase_id=None, service_id=None):
        try:
            purchase_item = db.session.query(PurchaseItem).filter_by(purchase_item_id=purchase_item_id).first()
            if purchase_id:
                purchase_item.purchase_id = purchase_id
            if service_id:
                purchase_item.service_id = service_id
            return purchase_item.purchase_item_id
        except Exception as e:
            raise e
        
class PurchaseVehical(db.Model):
    __tablename__ = 'purchase_vehical'

    purchase_vehical_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(INTEGER, ForeignKey('purchase.purchase_id'))
    vehical_id = Column(INTEGER, ForeignKey('vehical.vehical_id'))

    vehical = relationship('Vehical', back_populates='purchase_vehical')

    @classmethod
    def get_purchase_vehicals(cls):
        try:
            purchase_vehicals = db.session.query(PurchaseVehical).all()
            return purchase_vehicals
        except Exception as e:
            raise e

    @classmethod
    def get_purchase_vehical(cls, purchase_vehical_id):
        try:
            purchase_vehical = db.session.query(PurchaseVehical).filter_by(purchase_vehical_id=purchase_vehical_id).first()
            return purchase_vehical
        except Exception as e:
            raise e

    @classmethod
    def create_purchase_vehical(cls, purchase_id, vehical_id):
        try:
            purchase_vehical = PurchaseVehical(purchase_id=purchase_id, vehical_id=vehical_id)
            db.session.add(purchase_vehical)
            return purchase_vehical.purchase_vehical_id
        except Exception as e:
            raise e

    @classmethod
    def update_purchase_vehical(cls, purchase_vehical_id, purchase_id=None, vehical_id=None):
        try:
            purchase_vehical = db.session.query(PurchaseVehical).filter_by(purchase_vehical_id=purchase_vehical_id).first()
            if purchase_id:
                purchase_vehical.purchase_id = purchase_id
            if vehical_id:
                purchase_vehical.vehical_id = vehical_id
            return purchase_vehical.purchase_vehical_id
        except Exception as e:
            raise e