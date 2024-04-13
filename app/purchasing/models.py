# models.py

from app import db

class LoanRequest(db.Model):
    __tablename__ = 'loan_request'

    request_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    requested_loan_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Status of the loan request (e.g., pending, approved, rejected)

    customer = db.relationship('Customer')
    vehicle = db.relationship('Vehicle')

class PaymentHistory(db.Model):
    __tablename__ = 'payment_history'

    payment_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    loan_request_id = db.Column(db.Integer, db.ForeignKey('loan_request.request_id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)

    customer = db.relationship('Customer')
    loan_request = db.relationship('LoanRequest')
