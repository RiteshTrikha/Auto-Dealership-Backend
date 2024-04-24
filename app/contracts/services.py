from datetime import datetime
import os
from weasyprint import HTML
from flask import render_template, current_app
from app.contracts.models import Contract
from app import db


class ContractServices:

    def generate_purchase_contract(self, purchase_id, customer_name, year, make, model, vin):
        '''
        Generates a contract
        ---
        creates a contract record
        '''
        contract_data = {
            'customer_name': customer_name,
            'year': year,
            'make': make,
            'model': model,
            'vin': vin,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'customer_signature': '________________________',
            'dealer_signature': '________________________'
        }

        try:
            contract_path = os.path.join('app/data/contracts/', f'purchase_contract_{purchase_id}.pdf')
            os.makedirs(os.path.dirname(contract_path), exist_ok=True)
            html = render_template('contract_template.html', **contract_data)
            HTML(string=html).write_pdf(contract_path)

            contract = Contract.create_contract(purchase_id=purchase_id, 
                                                contract_type=Contract.ContractType.PURCHASE.value,
                                                contract_path=contract_path,
                                                signer_full_name=customer_name,
                                                vehicle_year=year,
                                                vehicle_make=make,
                                                vehicle_model=model,
                                                vehicle_vin=vin)
            db.session.commit()
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def get_contract(self, contract_id):
        '''
        Retrieves a contract
        ---
        returns the contract pdf file
        '''
        try:
            contract = Contract.get_contract(contract_id)
            if not contract:
                raise Exception('Contract not found')
            return contract.contract_path
        except Exception as e:
            current_app.logger.exception(e)
            raise e
            
    def customer_sign_contract(self, contract_id, signature):
        '''
        Signs a contract
        ---
        updates contract status to SIGNED and updates pdf with signature string.
        signature string is appended to the pdf file.
        '''
        try:
            contract = Contract.get_contract(contract_id)
            contract_data = {
                'customer_name': contract.signer_full_name,
                'year': contract.vehicle_year,
                'make': contract.vehicle_make,
                'model': contract.vehicle_model,
                'vin': contract.vehicle_vin,
                'date': contract.contract_date.strftime('%Y-%m-%d'),
                'customer_signature': signature,
                'dealer_signature': '________________________'
            }
            contract_path = contract.contract_path

            html = render_template('contract_template.html', **contract_data)
            HTML(string=html).write_pdf(contract_path)

            contract.contract_status = Contract.ContractStatus.CUSTOMER_SIGNED.value
            contract.customer_signature = signature
            db.session.commit()
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def dealer_sign_contract(self, contract_id, signature):
        '''
        Signs a contract
        ---
        updates contract status to SIGNED and updates pdf with signature string.
        signature string is appended to the pdf file.
        '''
        try:
            contract = Contract.get_contract(contract_id)
            contract_data = {
                'customer_name': contract.signer_full_name,
                'year': contract.vehicle_year,
                'make': contract.vehicle_make,
                'model': contract.vehicle_model,
                'vin': contract.vehicle_vin,
                'date': contract.contract_date.strftime('%Y-%m-%d'),
                'customer_signature': contract.customer_signature,
                'dealer_signature': signature
            }
            contract_path = contract.contract_path

            html = render_template('contract_template.html', **contract_data)
            HTML(string=html).write_pdf(contract_path)

            contract.contract_status = Contract.ContractStatus.APPROVED.value
            contract.dealer_signature = signature
            db.session.commit()
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e



