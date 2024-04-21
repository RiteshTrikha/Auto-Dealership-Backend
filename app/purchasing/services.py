from .models import Purchase, Finance, Payment
from app.exceptions import ExposedException
from app import db

class LoanService:
    def request_loan(self, customer_id, vehicle_id, requested_loan_amount):
        try:
            # Create a new finance record for a purchase
            finance = Finance(purchase_id=vehicle_id, # Assuming purchase_id correlates to vehicle_id for simplicity
                              loan_amount=requested_loan_amount, 
                              status='pending')
            db.session.add(finance)
            db.session.commit()
            return finance.finance_id
        except Exception as e:
            db.session.rollback()
            raise ExposedException('Failed to request loan. Please try again.', code=500)

    def get_loan_requests(self, customer_id):
        try:
            # Get all finance records associated with the customer's purchases
            finances = Finance.query.join(Purchase).filter(Purchase.customer_id == customer_id).all()
            return finances
        except Exception as e:
            raise ExposedException('Failed to retrieve loan requests.', code=500)

    def make_payment(self, customer_id, finance_id, amount_paid):
        try:
            # Record the payment in the payment history
            payment = Payment(purchase_id=finance_id, # Assuming purchase_id correlates to finance_id for simplicity
                              payment_amount=amount_paid)
            db.session.add(payment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ExposedException('Failed to make payment. Please try again.', code=500)
