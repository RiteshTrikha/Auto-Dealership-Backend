# services.py

from .models import LoanRequest, PaymentHistory
from app.exceptions import ExposedException
from app import db

class LoanService:
    def request_loan(self, customer_id, vehicle_id, requested_loan_amount):
        try:
            # Create a new loan request
            loan_request = LoanRequest(customer_id=customer_id, vehicle_id=vehicle_id, 
                                       requested_loan_amount=requested_loan_amount, status='pending')
            db.session.add(loan_request)
            db.session.commit()
            return loan_request.request_id
        except Exception as e:
            db.session.rollback()
            raise ExposedException('Failed to request loan. Please try again.', code=500)

    def get_loan_requests(self, customer_id):
        try:
            # Get all loan requests made by a customer
            loan_requests = LoanRequest.query.filter_by(customer_id=customer_id).all()
            return loan_requests
        except Exception as e:
            raise ExposedException('Failed to retrieve loan requests.', code=500)

    def make_payment(self, customer_id, loan_request_id, amount_paid):
        try:
            # Record the payment in the payment history
            payment = PaymentHistory(customer_id=customer_id, loan_request_id=loan_request_id, 
                                      amount_paid=amount_paid)
            db.session.add(payment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ExposedException('Failed to make payment. Please try again.', code=500)
