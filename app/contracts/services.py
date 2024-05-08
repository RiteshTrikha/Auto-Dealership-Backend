from datetime import datetime
import os
from weasyprint import HTML
from flask import render_template, current_app
from app.contracts.models import Contract
from app import db


class ContractServices:

    def generate_contract(self, purchase_id, is_finance=False):
        try:
            contract = Contract.get_contract_by_purchase(purchase_id)

            contract_data = {
                'customer_name': f'{contract.customer.first_name} {contract.customer.last_name}',
                'year': contract.vehicle.year,
                'make': contract.vehicle.make,
                'model': contract.vehicle.model,
                'vin': contract.vehicle.vin,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'customer_signature': '________________________',
                'dealer_signature': '________________________'
            }

            if is_finance:
                contract_data['finance_amount'] = contract.finance.loan_amount
                contract_data['finance_apr'] = contract.finance.apr * 100
                contract_data['finance_term'] = contract.finance.term
                contract_data['finance_down_payment'] = contract.finance.down_payment
                contract_data['finance_monthly_payment'] = contract.finance.monthly_payment
                contract_data['finance_total_payment'] = contract.finance.total_loan_amount
                template = 'finance_contract_template.html'
            else:
                template = 'contract_template.html'

            contract_path = os.path.join('app/data/contracts/', f'contract_{purchase_id}.pdf')
            os.makedirs(os.path.dirname(contract_path), exist_ok=True)
            html = render_template(template, **contract_data)
            HTML(string=html).write_pdf(contract_path)

            contract.contract_path = contract_path
            db.session.commit()
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
    
    def re_generate_contract(self, purchase_id, is_finance=False):
        '''
        Re-generates a contract
        ---
        updates pdf file with new contract data
        '''
        try:
            contract = Contract.get_contract_by_purchase(purchase_id)
            contract_data = {
                'customer_name': f'{contract.customer.first_name} {contract.customer.last_name}',
                'year': contract.vehicle.year,
                'make': contract.vehicle.make,
                'model': contract.vehicle.model,
                'vin': contract.vehicle.vin,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'customer_signature': contract.customer_signature if contract.customer_signature else '________________________',
                'dealer_signature': contract.dealer_signature if contract.dealer_signature else '________________________'
            }
            if is_finance:
                contract_data['finance_amount'] = contract.finance.loan_amount
                contract_data['finance_apr'] = contract.finance.apr * 100
                contract_data['finance_term'] = contract.finance.term
                contract_data['finance_down_payment'] = contract.finance.down_payment
                contract_data['finance_monthly_payment'] = contract.finance.monthly_payment
                contract_data['finance_total_payment'] = contract.finance.total_loan_amount
                template = 'finance_contract_template.html'
            else:
                template = 'contract_template.html'
            contract_path = contract.contract_path

            html = render_template(template, **contract_data)
            HTML(string=html).write_pdf(contract_path)
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e

    def get_contract_path(self, contract_id):
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
            
    def customer_sign_contract(self, contract_id, signature, is_finance=False):
        '''
        Signs a contract
        ---
        updates contract status to SIGNED and updates pdf with signature string.
        signature string is appended to the pdf file.
        '''
        try:
            contract = Contract.get_contract(contract_id)
            contract_data = {
                'customer_name': f'{contract.customer.first_name} {contract.customer.last_name}',
                'year': contract.vehicle.year,
                'make': contract.vehicle.make,
                'model': contract.vehicle.model,
                'vin': contract.vehicle.vin,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'customer_signature': signature,
                'dealer_signature': '________________________'
            }
            if is_finance:
                contract_data['finance_amount'] = contract.finance.loan_amount
                contract_data['finance_apr'] = contract.finance.apr * 100
                contract_data['finance_term'] = contract.finance.term
                contract_data['finance_down_payment'] = contract.finance.down_payment
                contract_data['finance_monthly_payment'] = contract.finance.monthly_payment
                contract_data['finance_total_payment'] = contract.finance.total_loan_amount
                template = 'finance_contract_template.html'
            else:
                template = 'contract_template.html'
            contract_path = contract.contract_path

            html = render_template(template, **contract_data)
            HTML(string=html).write_pdf(contract_path)

            contract.contract_status = Contract.ContractStatus.CUSTOMER_SIGNED.value
            contract.customer_signature = signature
            db.session.commit()
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def dealer_sign_contract(self, contract_id, signature, is_finance=False):
        '''
        Signs a contract
        ---
        updates contract status to SIGNED and updates pdf with signature string.
        signature string is appended to the pdf file.
        '''
        try:
            contract = Contract.get_contract(contract_id)
            contract_data = {
                'customer_name': f'{contract.customer.first_name} {contract.customer.last_name}',
                'year': contract.vehicle.year,
                'make': contract.vehicle.make,
                'model': contract.vehicle.model,
                'vin': contract.vehicle.vin,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'customer_signature': contract.customer_signature if contract.customer_signature else '________________________',
                'dealer_signature': signature
            }
            if is_finance:
                contract_data['finance_amount'] = contract.finance.loan_amount
                contract_data['finance_apr'] = contract.finance.apr * 100
                contract_data['finance_term'] = contract.finance.term
                contract_data['finance_down_payment'] = contract.finance.down_payment
                contract_data['finance_monthly_payment'] = contract.finance.monthly_payment
                contract_data['finance_total_payment'] = contract.finance.total_loan_amount
                template = 'finance_contract_template.html'
            else:
                template = 'contract_template.html'
            contract_path = contract.contract_path

            html = render_template(template, **contract_data)
            HTML(string=html).write_pdf(contract_path)

            contract.contract_status = Contract.ContractStatus.APPROVED.value
            contract.dealer_signature = signature
            db.session.commit()
            return contract_path
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e

    def get_contract_by_purchase(self, purchase_id):
        try:
            contract = Contract.get_contract_by_purchase(purchase_id)
            if not contract:
                raise Exception('Contract not found')
            return contract
        except Exception as e:
            current_app.logger.exception(e)
            raise e

