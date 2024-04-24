from decimal import Decimal
from flask import current_app, g
from app.contracts.models import Contract
from .models import Purchase, Finance, Payment, PurchaseAddon, Purchasevehicle
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
            # check if negotiation is accepted
            if negotiation.negotiation_status != 2: # ACCEPTED
                raise ExposedException('Negotiation is not accepted')
            # create a purchase
            purchase = Purchase.create_purchase(customer_id=customer_id)
            # create purchase vehicle
            db.session.commit()
            current_app.logger.info('created purchase with id: %s', purchase.purchase_id)
            purchase_vehicle = Purchasevehicle.create_purchase_vehicle(purchase_id=purchase.purchase_id,
                                                                       vehicle_id=negotiation.vehicle_id,
                                                                       offer_id=negotiation.offers[-1].offer_id)
            # set vehicle status to RESERVED
            negotiation.vehicle.update_vehicle_status(3) # RESERVED
            db.session.commit()
            return {'purchase_id': purchase.purchase_id, 'purchase_vehicle_id': purchase_vehicle.purchase_vehicle_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
    
    def get_purchases(self, customer_id):
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

                    } for purchase in purchases]
            }
            return purchases_dict
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        

    def get_purchase_details(self, customer_id, purchase_id):
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            purchase_dict = {
                'purchase_id': purchase.purchase_id,
                'purchase_status': purchase.PurchaseStatus(purchase.purchase_status).name,
                'purchase_vehicle': {
                    'vehicle_id': purchase.purchase_vehicle.vehicle.vehicle_id,
                    'year': purchase.purchase_vehicle.vehicle.year,
                    'make': purchase.purchase_vehicle.vehicle.make,
                    'model': purchase.purchase_vehicle.vehicle.model,
                    'vin': purchase.purchase_vehicle.vehicle.vin,
                    'price': purchase.purchase_vehicle.offer.offer_price
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
                'contracts': [{
                    'contract_id': contract.contract_id,
                    'contract_type': contract.ContractType(contract.contract_type).name,
                    'contract_status': contract.ContractStatus(contract.contract_status).name
                } for contract in purchase.contracts] if purchase.contracts else []

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
        
    def generate_purchase_contract(self, purchase_id, customer_id):
        '''
        Generates a purchase contract
        ---
        creates a contract record
        '''
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            
            # check if purchase contract already exists
            if next((contract for contract in purchase.contracts if contract.contract_type == Contract.ContractType.PURCHASE.value), None):
                raise ExposedException('Contract already exists')
            
            contract_path = g.contract_service.generate_purchase_contract(purchase_id=purchase_id, 
                                                          customer_name=purchase.customer.first_name + '_' + purchase.customer.last_name,
                                                          year=purchase.purchase_vehicle.vehicle.year,
                                                          make=purchase.purchase_vehicle.vehicle.make,
                                                          model=purchase.purchase_vehicle.vehicle.model,
                                                          vin=purchase.purchase_vehicle.vehicle.vin)
            db.session.commit()
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
    
    def get_purchase_contract(self, purchase_id, customer_id):
        '''
        Retrieves a purchase contract
        ---
        returns the contract pdf file
        '''
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            contracts = purchase.contracts
            purchase_contract = next((contract for contract in contracts if contract.contract_type == Contract.ContractType.PURCHASE.value), None)
            return purchase_contract.contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def customer_sign_purchase_contract(self, customer_id, purchase_id, signature):
        '''
        Signs a purchase contract
        ---
        updates contract status to SIGNED
        '''
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if purchase belongs to customer
            if purchase.customer_id != customer_id:
                raise ExposedException('Unauthorized')
            # check if contract has been signed
            purchase_contract = next((contract for contract in purchase.contracts if contract.contract_type == Contract.ContractType.PURCHASE.value), None)
            if purchase_contract is None:
                raise ExposedException('contract does not exist')
            
            # get contract id
            contract_id = purchase_contract.contract_id
            contract_path = g.contract_service.customer_sign_contract(contract_id=contract_id, signature=signature)

            return contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    def dealer_sign_purchase_contract(self, purchase_id, signature):
        '''
        Signs a purchase contract
        ---
        updates contract status to SIGNED
        '''
        try:
            purchase = Purchase.get_purchase(purchase_id)
            # check if contract has been signed
            if purchase.contract.contract_status != Contract.ContractStatus.CUSTOMER_SIGNED.value:
                raise ExposedException('contract has not been signed')
            
            # get contract id
            contract_id = purchase.contract.contract_id
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
            if routing_number.length != 9 or not routing_number.isdigit():
                raise ExposedException('Invalid routing number')
            if not account_number.length >= 8 or not account_number.length <= 12:
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
            if next((contract for contract in purchase.contracts if contract.contract_status != Contract.ContractStatus.APPROVED.value), None):
                raise ExposedException('contract has not been approved')
            # check if purchase exists and is not paid
            if not purchase or purchase.purchase_status == Purchase.PurchaseStatus.PAID.value:
                raise ExposedException('purchase does not exist or is already paid')
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
            db.session.commit()
            return {'payment_id': payment.payment_id}
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