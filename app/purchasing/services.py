from decimal import Decimal
import os
from flask import current_app, g
from app.contracts.models import Contract
from .models import Purchase, Finance, Payment, PurchaseAddon, Purchasevehicle
from app.customer.models import CustomerVehicle, CreditReport
from app.exceptions import ExposedException
from app import db

class PurchasingServices:

    def initiate_car_purchase(self, customer_id, negotiation_id):
        '''
        Initiates a car purchase from an accepted negotiation
        ---
        checks if negotiation is accepted
        checks if vehicle is available
        creates a purchase record
        creates a purchase vehicle record
        updates vehicle status to RESERVED
        '''
        try:
            # get accepted negotiation
            negotiation = g.negotiation_service.get_accepted_negotiation(customer_id, negotiation_id)

            # create a purchase
            purchase = Purchase.create_purchase(customer_id=customer_id,
                                                negotiation_id=negotiation_id,
                                                purchase_type=Purchase.PurchaseType.CAR_PURCHASE.value)

            db.session.commit()
            return {'purchase_id': purchase.purchase_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
    
    def get_purchases(self):
        try:
            purchases = Purchase.get_purchases()
            purchases_dict = {
                'purchases': [
                    {
                        'customer': {
                            'customer_id': purchase.customer.customer_id,
                            'first_name': purchase.customer.first_name,
                            'last_name': purchase.customer.last_name
                        },
                        'purchase_id': purchase.purchase_id,
                        'purchase_status': purchase.PurchaseStatus(purchase.purchase_status).name,
                        'purchase_vehicle': {
                            'vehicle_id': purchase.purchase_vehicle.vehicle.vehicle_id,
                            'year': purchase.purchase_vehicle.vehicle.year,
                            'make': purchase.purchase_vehicle.vehicle.make,
                            'model': purchase.purchase_vehicle.vehicle.model,
                        },
                        'puchase_total': '{:.2f}'.format(purchase.get_purchase_totals()[0])
                    } for purchase in purchases]
            }
            return purchases_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e
    
    def get_purchases_with_dates(self):
        try:
            purchases = Purchase.get_purchases()
            purchases_dict = {
                'purchases': [
                    {
                        'customer': {
                            'customer_id': purchase.customer.customer_id,
                            'first_name': purchase.customer.first_name,
                            'last_name': purchase.customer.last_name
                        },
                        'purchase_id': purchase.purchase_id,
                        'purchase_status': purchase.PurchaseStatus(purchase.purchase_status).name,
                        'purchase_vehicle': {
                            'vehicle_id': purchase.purchase_vehicle.vehicle.vehicle_id,
                            'year': purchase.purchase_vehicle.vehicle.year,
                            'make': purchase.purchase_vehicle.vehicle.make,
                            'model': purchase.purchase_vehicle.vehicle.model,
                        },
                        'purchase_total': '{:.2f}'.format(purchase.get_purchase_totals()[0]),
                        'open_date': purchase.open_date.isoformat() if purchase.open_date else None,
                        'close_date': purchase.close_date.isoformat() if purchase.close_date else None,
                        'is_open': purchase.is_open
                    } for purchase in purchases]
            }
            return purchases_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e


    def get_customer_purchases(self, customer_id):
        try:
            purchases = Purchase.get_customer_purchases(customer_id)
            purchases_dict = {
                'purchases': [
                    {
                        'purchase_id': purchase.purchase_id,
                        'purchase_status': purchase.PurchaseStatus(purchase.purchase_status).name,
                        'purchase_vehicle': {
                            'vehicle_id': purchase.purchase_vehicle.vehicle.vehicle_id,
                            'year': purchase.purchase_vehicle.vehicle.year,
                            'make': purchase.purchase_vehicle.vehicle.make,
                            'model': purchase.purchase_vehicle.vehicle.model,
                        },
                        'puchase_total': '{:.2f}'.format(purchase.get_purchase_totals()[0]),
                        'open_date': purchase.open_date.isoformat() if purchase.open_date else None,
                        'close_date': purchase.close_date.isoformat() if purchase.close_date else None,
                        'is_open': purchase.is_open
                    } for purchase in purchases]
            }
            return purchases_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def get_purchase_details(self, purchase_id):
        try:
            purchase = Purchase.get_purchase(purchase_id)
            contract = g.contract_service.get_contract_by_purchase(purchase_id)
            purchase_dict = {
                'customer': {
                    'customer_id': purchase.customer.customer_id,
                    'first_name': purchase.customer.first_name,
                    'last_name': purchase.customer.last_name
                },
                'purchase_id': purchase.purchase_id,
                'purchase_status': purchase.PurchaseStatus(purchase.purchase_status).name,
                'purchase_vehicle': {
                    'vehicle_id': purchase.purchase_vehicle.vehicle.vehicle_id,
                    'year': purchase.purchase_vehicle.vehicle.year,
                    'make': purchase.purchase_vehicle.vehicle.make,
                    'model': purchase.purchase_vehicle.vehicle.model,
                    'vin': purchase.purchase_vehicle.vehicle.vin,
                    'price': purchase.purchase_vehicle.offer.offer_price,
                    'status': purchase.purchase_vehicle.vehicle.VehicleStatus(purchase.purchase_vehicle.vehicle.vehicle_status).name
                },
                'purchase_subtotal': '{:.2f}'.format(purchase.get_purchase_totals()[1]),
                'tax': purchase.tax,
                'puchase_total': '{:.2f}'.format(purchase.get_purchase_totals()[0]),
                'addons': [{
                    'addon_id': pa.addon.addon_id,
                    'name': pa.addon.addon_name,
                    'price': pa.addon.price,
                    'description': pa.addon.description
                } for pa in purchase.purchase_addons] if purchase.purchase_addons else [],
                'finance': {
                    'finance_id': purchase.finance.finance_id if purchase.finance else None
                },
                'open_date': purchase.open_date.isoformat() if purchase.open_date else None,
                'close_date': purchase.close_date.isoformat() if purchase.close_date else None,
                'is_open': purchase.is_open,
                'payment_type': purchase.PaymentType(purchase.payment_type).name if purchase.payment_type else None,
                'customer_signed': contract.customer_signed if contract else False,
                'dealer_signed': contract.dealer_signed if contract else False

            }
            return purchase_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    def get_customer_purchase_details(self, customer_id, purchase_id):
        try:
            purchase = Purchase.get_purchase(purchase_id)
            contract = g.contract_service.get_contract_by_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            purchase_dict = {
                'customer': {
                    'customer_id': purchase.customer.customer_id,
                    'first_name': purchase.customer.first_name,
                    'last_name': purchase.customer.last_name
                },
                'purchase_id': purchase.purchase_id,
                'purchase_status': purchase.PurchaseStatus(purchase.purchase_status).name,
                'purchase_vehicle': {
                    'vehicle_id': purchase.purchase_vehicle.vehicle.vehicle_id,
                    'year': purchase.purchase_vehicle.vehicle.year,
                    'make': purchase.purchase_vehicle.vehicle.make,
                    'model': purchase.purchase_vehicle.vehicle.model,
                    'vin': purchase.purchase_vehicle.vehicle.vin,
                    'price': purchase.purchase_vehicle.offer.offer_price,
                    'status': purchase.purchase_vehicle.vehicle.VehicleStatus(purchase.purchase_vehicle.vehicle.vehicle_status).name
                },
                'purchase_subtotal': '{:.2f}'.format(purchase.get_purchase_totals()[1]),
                'tax': purchase.tax,
                'puchase_total': '{:.2f}'.format(purchase.get_purchase_totals()[0]),
                'addons': [{
                    'addon_id': pa.addon.addon_id,
                    'name': pa.addon.addon_name,
                    'price': pa.addon.price,
                    'description': pa.addon.description
                } for pa in purchase.purchase_addons] if purchase.purchase_addons else [],
                'finance': {
                    'finance_id': purchase.finance.finance_id if purchase.finance else None
                },
                'open_date': purchase.open_date.isoformat() if purchase.open_date else None,
                'close_date': purchase.close_date.isoformat() if purchase.close_date else None,
                'is_open': purchase.is_open,
                'payment_type': purchase.PaymentType(purchase.payment_type).name if purchase.payment_type else None,
                'customer_signed': contract.customer_signed if contract else False,
                'dealer_signed': contract.dealer_signed if contract else False

            }
            return purchase_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    # add addons to a purchase
    def add_addons_to_purchase(self, customer_id, purchase_id, addon_ids):
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            purchase_addons = []
            for addon_id in addon_ids:
                purchase_addon = PurchaseAddon.create_purchase_addon(purchase_id=purchase_id, addon_id=addon_id)
                if not purchase_addon:
                    raise ExposedException('Failed to add addon(s)')
                purchase_addons.append(purchase_addon)
            db.session.commit()
            return {'purchase_addons': [pa.addon_id for pa in purchase_addons]}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
    
    def generate_finance_contract(self, purchase_id, customer_id):
        try:

            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            
            # check if customer has a credit report
            credit_report = g.customer_service.get_credit_report_by_customer(customer_id)
            current_app.logger.info('credit report: %s', credit_report)
            if not credit_report:
                raise ExposedException('No credit report found. You do not qualify for financing')

            # create finance record
            if purchase.finance is None:
                finance = Finance.create_finance(purchase_id=purchase_id, loan_amount=purchase.get_purchase_totals()[0],
                                            apr=credit_report.apr, term=36)
            else:
                finance = purchase.finance
            
            current_app.logger.info('finance id: %s', finance.finance_id)

            # update purchase payment type to finance
            purchase.payment_type = Purchase.PaymentType.FINANCE.value
            db.session.commit()
            
            contract_path = g.contract_service.generate_contract(purchase_id=purchase_id, is_finance=True)

            return contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    def generate_purchase_contract(self, purchase_id, customer_id):
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')

            purchase.payment_type = Purchase.PaymentType.ACH.value

            contract_path = g.contract_service.generate_contract(purchase_id=purchase_id, is_finance=False)

            return contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e
    
    def get_contract(self, purchase_id, customer_id=None):
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if customer_id:
                if purchase.customer_id != customer_id:
                    raise ExposedException('Unauthorized')
            
            is_finance = purchase.payment_type == Purchase.PaymentType.FINANCE.value

            contract_path = g.contract_service.re_generate_contract(purchase_id=purchase_id, is_finance=is_finance)

            return contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e
    
    def customer_sign_contract(self, purchase_id, customer_id, signature):
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            
            contract = g.contract_service.get_contract_by_purchase(purchase_id)
            if not contract:
                raise ExposedException('Contract does not exist. Please generate contract first')

            # get contract id
            contract_id = contract.contract_id
            contract_path = g.contract_service.customer_sign_contract(contract_id=contract_id, signature=signature)

            return contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def dealer_sign_contract(self, purchase_id, signature):
        try:
            purchase = Purchase.get_purchase(purchase_id)

            # check if contract exists
            contract = g.contract_service.get_contract_by_purchase(purchase_id)
            if not contract:
                raise ExposedException('Contract does not exist')
            
            # get contract id
            contract_id = contract.contract_id
            contract_path = g.contract_service.dealer_sign_contract(contract_id=contract_id, signature=signature)

            return contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    def validate_bank_account_details(self, account_number, routing_number):
        '''
        Verifies account number and routing number for ACH payment
        '''
        try:
            # account and routing number come as strings which have no attribute length or Length
            if len(routing_number) != 9 or not routing_number.isdigit():
                raise ExposedException('Invalid routing number')
            if not len(account_number) >= 8 or not len(account_number) <= 12:
                raise ExposedException('Invalid account number')
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def finance_purchase(self, customer_id, purchase_id, finance_id):
        pass #TODO implement finance purchase


    def pay_purchase_ACH(self, customer_id, purchase_id, account_number, routing_number):
        '''
        Makes an ACH payment for a purchase
        ---
        creates a payment record and updates the purchase status to PAID and vehicle status to SOLD
        '''
        try:
            # Ensure this method is fetching and checking the purchase correctly
            purchase = Purchase.get_purchase(purchase_id)
            if not purchase:
                raise ExposedException('Purchase does not exist')

            if purchase.purchase_status == Purchase.PurchaseStatus.PAID.value:
                raise ExposedException('Purchase is already paid')

            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            
            #check that purchase is an ACH purchase
            if purchase.payment_type != Purchase.PaymentType.ACH.value:
                raise ExposedException('Invalid payment type. please generate and sign a purchase contract')

            contract = g.contract_service.get_contract_by_purchase(purchase_id)
            current_app.logger.info('Contract signed: %s', contract.customer_signed)
            if not contract or contract.customer_signed != 1 or contract.dealer_signed != 1:
                raise ExposedException('Contract not signed')

            self.validate_bank_account_details(account_number, routing_number)
            purchase_total, _ = purchase.get_purchase_totals()

            # Ensure that payment creation is handled correctly
            payment = Payment.create_payment(purchase_id=purchase_id, finance_id=None,
                                            account_number=account_number,
                                            routing_number=routing_number,
                                            payment_amount=purchase_total)

            purchase.update_purchase_status(Purchase.PurchaseStatus.PAID.value)
            purchase.purchase_vehicle.vehicle.update_vehicle_status(2)  # SOLD

            # get rid of finance record if it exists
            if purchase.finance:
                db.session.delete(purchase.finance)
                db.session.commit()

            # Handling vehicle creation without immediate commit
            customer_vehicle = g.customer_service.create_customer_vehicle_no_commit(
                customer_id=customer_id,
                vin=purchase.purchase_vehicle.vehicle.vin,
                year=purchase.purchase_vehicle.vehicle.year,
                make=purchase.purchase_vehicle.vehicle.make,
                model=purchase.purchase_vehicle.vehicle.model
            )
            db.session.flush()
            # Addons loop, make sure it is syntactically correct
            for addon in purchase.purchase_addons:
                g.customer_service.create_customer_addon(customer_id=customer_id, addon_id=addon.addon_id,
                                                            customer_vehicle_id=customer_vehicle.customer_vehicle_id)

            db.session.commit()
            return {'payment_id': payment.payment_id, 'customer_vehicle_id': customer_vehicle.customer_vehicle_id}
        except Exception as e:
            db.session.rollback()
            existing_vehicle = CustomerVehicle.query.filter_by(vin=purchase.purchase_vehicle.vehicle.vin).first()
            if existing_vehicle:
                db.session.delete(existing_vehicle)
                db.session.flush()  # Flush here to ensure deletion is executed immediately
            purchase.update_purchase_status(Purchase.PurchaseStatus.ACTIVE.value)
            purchase.purchase_vehicle.vehicle.update_vehicle_status(1)  # AVAILABLE
            db.session.commit()
            current_app.logger.exception(e)
            raise e

    def pay_purchase_down_payment(self, customer_id, purchase_id, account_number, routing_number):
        '''
        Makes an ACH payment for a purchase
        ---
        creates a payment record and updates the purchase status to PAID and vehicle status to SOLD
        '''
        try:
            # Ensure this method is fetching and checking the purchase correctly
            purchase = Purchase.get_purchase(purchase_id)
            if not purchase:
                raise ExposedException('Purchase does not exist')

            if purchase.purchase_status == Purchase.PurchaseStatus.PAID.value:
                raise ExposedException('Purchase is already paid')

            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            
            #check that purchase is an FINANCE purchase
            if purchase.payment_type != Purchase.PaymentType.FINANCE.value:
                raise ExposedException('Invalid payment type. please generate and sign a finance contract')

            contract = g.contract_service.get_contract_by_purchase(purchase_id)
            current_app.logger.info('Contract signed: %s', contract.customer_signed)
            if not contract or contract.customer_signed != 1 or contract.dealer_signed != 1:
                raise ExposedException('Contract not signed')

            finance = purchase.finance

            if not finance:
                raise ExposedException('Finance record does not exist. Please generate a finance contract')

            self.validate_bank_account_details(account_number, routing_number)
            down_payment = finance.down_payment

            # Ensure that payment creation is handled correctly
            payment = Payment.create_payment(purchase_id=purchase_id, finance_id=None,
                                            account_number=account_number,
                                            routing_number=routing_number,
                                            payment_amount=down_payment)

            purchase.update_purchase_status(Purchase.PurchaseStatus.PAID.value)
            purchase.purchase_vehicle.vehicle.update_vehicle_status(2)  # SOLD


            # Handling vehicle creation without immediate commit
            customer_vehicle = g.customer_service.create_customer_vehicle_no_commit(
                customer_id=customer_id,
                vin=purchase.purchase_vehicle.vehicle.vin,
                year=purchase.purchase_vehicle.vehicle.year,
                make=purchase.purchase_vehicle.vehicle.make,
                model=purchase.purchase_vehicle.vehicle.model
            )
            db.session.flush()
            # Addons loop
            for addon in purchase.purchase_addons:
                g.customer_service.create_customer_addon(customer_id=customer_id, addon_id=addon.addon_id,
                                                            customer_vehicle_id=customer_vehicle.customer_vehicle_id)

            db.session.commit()
            return {'payment_id': payment.payment_id, 'customer_vehicle_id': customer_vehicle.customer_vehicle_id}
        except Exception as e:
            db.session.rollback()
            existing_vehicle = CustomerVehicle.query.filter_by(vin=purchase.purchase_vehicle.vehicle.vin).first()
            if existing_vehicle:
                db.session.delete(existing_vehicle)
                db.session.flush()  # Flush here to ensure deletion is executed immediately
            purchase.update_purchase_status(Purchase.PurchaseStatus.ACTIVE.value)
            purchase.purchase_vehicle.vehicle.update_vehicle_status(1)  # AVAILABLE
            db.session.commit()
            current_app.logger.exception(e)
            raise e
        
    def cancel_purchase(self, customer_id, purchase_id):
        '''
        Cancels a purchase
        ---
        updates purchase status to CANCELLED and vehicle status to AVAILABLE
        '''
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase exists and is not paid
            if not purchase or purchase.purchase_status == Purchase.PurchaseStatus.PAID.value:
                raise ExposedException('purchase does not exist or is already paid')
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            purchase.update_purchase_status(Purchase.PurchaseStatus.CANCELLED.value)
            # update vehicle status
            purchase.purchase_vehicle.vehicle.update_vehicle_status(1) # AVAILABLE
            db.session.commit()
            return {'purchase_id': purchase.purchase_id, 'purchase_status': purchase.PurchaseStatus(purchase.purchase_status).name}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        

    ####### Finance Services ########

    def get_finances(self):
        try:
            finances = Finance.get_finances()
            finances_dict = {
                'finances': [
                    {
                        'finance_id': finance.finance_id,
                        'purchase_id': finance.purchase_id,
                        'start_date': finance.start_date.isoformat(),
                        'end_date': finance.end_date.isoformat() if finance.end_date else None,
                        'loan_amount': finance.loan_amount,
                        'down_payment': finance.down_payment,
                        'total_loan_amount': finance.total_loan_amount,
                        'monthly_payment': finance.monthly_payment,
                        'apr': finance.apr,
                        'term': finance.term,
                        'paid': finance.paid,
                        'finance_status': finance.FinanceStatus(finance.finance_status).name if finance.finance_status else None
                    } for finance in finances]
            }
            return finances_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def get_customer_finances(self, customer_id):
        try:
            finances = Finance.get_finances_by_customer(customer_id)
            finances_dict = {
                'finances': [
                    {
                        'finance_id': finance.finance_id,
                        'purchase_id': finance.purchase_id,
                        'start_date': finance.start_date.isoformat(),
                        'end_date': finance.end_date.isoformat() if finance.end_date else None,
                        'loan_amount': finance.loan_amount,
                        'down_payment': finance.down_payment,
                        'total_loan_amount': finance.total_loan_amount,
                        'monthly_payment': finance.monthly_payment,
                        'apr': finance.apr,
                        'term': finance.term,
                        'paid': finance.paid,
                        'finance_status': finance.FinanceStatus(finance.finance_status).name if finance.finance_status else None
                    } for finance in finances]
            }
            return finances_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def get_finance_details(self, finance_id):
        try:
            finance = Finance.get_finance(finance_id)
            finance_dict = {
                'finance_id': finance.finance_id,
                'purchase_id': finance.purchase_id,
                'start_date': finance.start_date.isoformat(),
                'end_date': finance.end_date.isoformat() if finance.end_date else None,
                'loan_amount': finance.loan_amount,
                'down_payment': finance.down_payment,
                'total_loan_amount': finance.total_loan_amount,
                'monthly_payment': finance.monthly_payment,
                'apr': finance.apr,
                'term': finance.term,
                'paid': finance.paid,
                'finance_status': finance.FinanceStatus(finance.finance_status).name if finance.finance_status else None
            }
            return finance_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e