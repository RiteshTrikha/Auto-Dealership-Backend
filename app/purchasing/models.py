from flask import current_app
from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import Enum


class Purchase(db.Model):
    __tablename__ = 'purchase'

    class PurchaseStatus(Enum):
        PAID = 0
        ACTIVE = 1
        CANCELLED = 2

    class PurchaseType(Enum):
        CAR_PURCHASE = 0
        SERVICE_PURCHASE = 1

    class PaymentType(Enum):
        ACH = 0
        FINANCE = 1

    purchase_id = Column(INTEGER, primary_key=True, unique=True)
    customer_id = Column(INTEGER, ForeignKey('customer.customer_id'))
    negotiation_id = Column(INTEGER, ForeignKey('negotiation.negotiation_id'))
    open_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    close_date = Column(DateTime)
    is_open = Column(INTEGER, server_default=text("1"))
    payment_type = Column(INTEGER)
    purchase_type = Column(INTEGER)
    purchase_status = Column(INTEGER)
    tax = Column(Float)

    customer = relationship('app.customer.models.Customer', backref='purchase', uselist=False)
    finance = relationship('Finance', backref='purchase', uselist=False)
    payment = relationship('Payment', backref='purchase', uselist=False)
    purchase_addons = relationship('PurchaseAddon', backref='purchase')
    purchase_vehicle = relationship('Purchasevehicle', backref='purchase', uselist=False)

    def get_purchase_totals(self):
        try:
            sub_total = 0

            if self.purchase_addons:
                for purchase_addon in self.purchase_addons:
                    sub_total += purchase_addon.addon.price

            if self.purchase_vehicle.offer.offer_price:
                sub_total += self.purchase_vehicle.offer.offer_price

            total = sub_total + (sub_total * self.tax)
            return total, sub_total
        except Exception as e:
            raise e

    @classmethod
    def get_purchases(cls):
        try:
            purchases = db.session.query(Purchase).all()
            return purchases
        except Exception as e:
            raise e
        
    @classmethod
    def get_customer_purchases(cls, customer_id):
        try:
            purchases = db.session.query(Purchase).filter_by(customer_id=customer_id).all()
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
    def get_purchase_by_customer(cls, purchase_id, customer_id):
        try:
            purchase = db.session.query(Purchase).filter_by(purchase_id=purchase_id, customer_id=customer_id).first()
            return purchase
        except Exception as e:
            raise e

    @classmethod
    def create_purchase(cls, customer_id, purchase_type, tax=0.06625, negotiation_id=None):
        try:
            purchase = Purchase(customer_id=customer_id,
                                negotiation_id=negotiation_id,
                                purchase_type=purchase_type,
                                purchase_status=cls.PurchaseStatus.ACTIVE.value,
                                tax=tax)
            db.session.add(purchase)
            return purchase
        except Exception as e:
            raise e
        
    def update_purchase_status(self, status):
        try:
            self.purchase_status = status
            return self
        except Exception as e:
            raise e
    
    def update_purchase_type(self, purchase_type):
        try:
            self.purchase_type = purchase_type
            return self
        except Exception as e:
            raise e

    @classmethod
    def update_purchase(cls, purchase_id, tax=None, 
                        purchase_status=None, close_date=None, purchase_type=None):
        try:
            purchase = db.session.query(Purchase).filter_by(purchase_id=purchase_id).first()
            if tax:
                purchase.tax = tax
            if purchase_status:
                purchase.purchase_status = purchase_status
            if close_date:
                purchase.close_date = close_date
            if purchase_type:
                purchase.purchase_type = purchase_type
            return purchase.purchase_id
        except Exception as e:
            raise e

class Finance(db.Model):
    __tablename__ = 'finance'

    class FinanceStatus(Enum):
        ACTIVE = 0
        PAID = 1

    finance_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(INTEGER, ForeignKey('purchase.purchase_id'), unique=True)
    start_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    end_date = Column(DateTime)
    loan_amount = Column(INTEGER)
    down_payment = Column(INTEGER)
    total_loan_amount = Column(INTEGER)
    monthly_payment = Column(INTEGER)
    apr = Column(Float)
    term = Column(INTEGER)
    paid = Column(INTEGER)
    finance_status = Column(INTEGER, server_default=text("0"))

    payment = relationship('Payment', backref='finance')

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
    def get_finance_by_purchase(cls, purchase_id):
        try:
            finance = db.session.query(Finance).filter_by(purchase_id=purchase_id).first()
            return finance
        except Exception as e:
            raise e

    @classmethod
    def create_finance(cls, purchase_id, loan_amount, apr, 
                       term):
        try:
            down_payment = loan_amount * 0.2
            total_loan_amount = (loan_amount - down_payment) * (1 + apr) ** term
            monthly_payment = total_loan_amount / term

            finance = Finance(purchase_id=purchase_id, loan_amount=loan_amount, 
                              apr=apr, term=term,
                              down_payment=down_payment, total_loan_amount=total_loan_amount,
                              monthly_payment=monthly_payment)
            db.session.add(finance)
            db.session.commit()
            return finance
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def update_finance(cls, finance_id, purchase_id=None, start_date=None, end_date=None, 
                       down_payment=None, loan_amount=None, apr=None, term=None, paid=None):
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
            if apr:
                finance.apr = apr
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
            return payment
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
            return payment
        except Exception as e:
            raise e
        
class PurchaseAddon(db.Model):
    __tablename__ = 'purchase_addon'

    purchase_addon_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(INTEGER, ForeignKey('purchase.purchase_id'))
    addon_id = Column(INTEGER, ForeignKey('addon.addon_id'))

    addon = relationship('app.inventory.models.Addon', backref='purchase_addon')

    @classmethod
    def get_purchase_addons(cls):
        try:
            purchase_addons = db.session.query(PurchaseAddon).all()
            return purchase_addons
        except Exception as e:
            raise e

    @classmethod
    def get_purchase_addon(cls, purchase_addon_id):
        try:
            purchase_addon = db.session.query(PurchaseAddon).filter_by(purchase_addon_id=purchase_addon_id).first()
            return purchase_addon
        except Exception as e:
            raise e

    @classmethod
    def create_purchase_addon(cls, purchase_id, addon_id):
        try:
            purchase_addon = PurchaseAddon(purchase_id=purchase_id, addon_id=addon_id)
            db.session.add(purchase_addon)
            return purchase_addon
        except Exception as e:
            raise e

    @classmethod
    def update_purchase_addon(cls, purchase_addon_id, purchase_id=None, addon_id=None):
        try:
            purchase_addon = db.session.query(PurchaseAddon).filter_by(purchase_addon_id=purchase_addon_id).first()
            if purchase_id:
                purchase_addon.purchase_id = purchase_id
            if addon_id:
                purchase_addon.addon_id = addon_id
            return purchase_addon.purchase_addon_id
        except Exception as e:
            raise e
        
class Purchasevehicle(db.Model):
    __tablename__ = 'purchase_vehicle'

    purchase_vehicle_id = Column(INTEGER, primary_key=True, unique=True)
    purchase_id = Column(INTEGER, ForeignKey('purchase.purchase_id'))
    vehicle_id = Column(INTEGER, ForeignKey('vehicle.vehicle_id'))
    offer_id = Column(INTEGER, ForeignKey('offer.offer_id'))

    vehicle = relationship('app.inventory.models.Vehicle', backref='purchase_vehicle')
    offer = relationship('app.negotiation.models.Offer', backref='purchase_vehicle')

    @classmethod
    def get_purchase_vehicles(cls):
        try:
            purchase_vehicles = db.session.query(Purchasevehicle).all()
            return purchase_vehicles
        except Exception as e:
            raise e

    @classmethod
    def get_purchase_vehicle(cls, purchase_vehicle_id):
        try:
            purchase_vehicle = db.session.query(Purchasevehicle).filter_by(purchase_vehicle_id=purchase_vehicle_id).first()
            return purchase_vehicle
        except Exception as e:
            raise e

    @classmethod
    def create_purchase_vehicle(cls, purchase_id, vehicle_id, offer_id):
        try:
            purchase_vehicle = Purchasevehicle(purchase_id=purchase_id, vehicle_id=vehicle_id, 
                                               offer_id=offer_id)
            db.session.add(purchase_vehicle)
            return purchase_vehicle
        except Exception as e:
            raise e

    @classmethod
    def update_purchase_vehicle(cls, purchase_vehicle_id, purchase_id=None, vehicle_id=None):
        try:
            purchase_vehicle = db.session.query(Purchasevehicle).filter_by(purchase_vehicle_id=purchase_vehicle_id).first()
            if purchase_id:
                purchase_vehicle.purchase_id = purchase_id
            if vehicle_id:
                purchase_vehicle.vehicle_id = vehicle_id
            return purchase_vehicle.purchase_vehicle_id
        except Exception as e:
            raise e