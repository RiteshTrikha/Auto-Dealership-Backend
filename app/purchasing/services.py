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
                    'status': purchase.purchase_vehicle.VehicleStatus(purchase.purchase_vehicle.vehicle.status).name
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
            purchase_contract = next((contract for contract in purchase.contracts if contract.contract_type == Contract.ContractType.PURCHASE.value), None)
            if purchase_contract is None:
                raise ExposedException('contract does not exist')
            current_app.logger.info('contract status: %s contract type: %s', purchase_contract.contract_status, purchase_contract.contract_type)
            if purchase_contract.contract_status == Contract.ContractStatus.APPROVED.value:
                raise ExposedException('contract already signed')
            if purchase_contract.contract_status == Contract.ContractStatus.ACTIVE.value:
                raise ExposedException('contract must be signed by customer before dealer can sign')
            
            # get contract id
            contract_id = purchase_contract.contract_id
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
            purchase = Purchase.get_purchase(purchase_id)
            # check if contract has been signed
            if next((contract for contract in purchase.contracts if contract.contract_status == Contract.ContractStatus.APPROVED.value), None):
                raise ExposedException('contract has not been approved')
            # check if purchase exists and is not paid
            if not purchase:
                raise ExposedException('purchase does not exist')
            if purchase.purchase_status == Purchase.PurchaseStatus.PAID.value:
                raise ExposedException('purchase is already paid')
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            # validate account details
            self.validate_bank_account_details(account_number, routing_number)

            # get purchase total
            purchase_total, _ = purchase.get_purchase_totals()
            # create payment
            payment = Payment.create_payment(purchase_id=purchase_id, finance_id=None,
                                             account_number=account_number,
                                             routing_number=routing_number,
                                             payment_amount=purchase_total)
            # update purchase type and status
            purchase.update_purchase_type(Purchase.PurchaseType.ACH.value)
            purchase.update_purchase_status(Purchase.PurchaseStatus.PAID.value)

            # update vehicle status
            purchase.purchase_vehicle.vehicle.update_vehicle_status(2) # SOLD

            # add vehicle to customer's vehicles
            customer_vehicle = g.customer_service.create_customer_vehicle(customer_id=customer_id,
                                                                      vin=purchase.purchase_vehicle.vehicle.vin,
                                                                      year=purchase.purchase_vehicle.vehicle.year,
                                                                      make=purchase.purchase_vehicle.vehicle.make,
                                                                      model=purchase.purchase_vehicle.vehicle.model)

            db.session.commit()
            return {'payment_id': payment.payment_id, 'customer_vehicle_id': customer_vehicle.customer_vehicle_id}
        except Exception as e:
            db.session.rollback()
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
            return {'purchase_id': purchase.purchase_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e