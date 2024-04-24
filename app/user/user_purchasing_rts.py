from flask import request, current_app, g, send_file
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from . import user_bp
from app.auth.auth_decorators import manager_required

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response


# get all purchases
@user_bp.route('/purchases', methods=['GET'])
@swag_from({
    'summary': 'Get all purchases',
    'tags': ['User Purchasing'],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'All purchases',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'purchases': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'customer': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'customer_id': {'type': 'integer'},
                                                        'first_name': {'type': 'string'},
                                                        'last_name': {'type': 'string'}
                                                    }
                                                },
                                                'purchase_id': {'type': 'integer'},
                                                'purchase_status': {'type': 'string'},
                                                'purchase_vehicle': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'vehicle_id': {'type': 'integer'},
                                                        'year': {'type': 'integer'},
                                                        'make': {'type': 'string'},
                                                        'model': {'type': 'string'},
                                                    }
                                                },
                                                'purchase_total': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def get_purchases():
    try:
        purchases_dict = g.purchasing_service.get_purchases()
        return standardize_response(data=purchases_dict)
    except Exception as e:
        raise e
    
# get purchase details
@user_bp.route('/purchases/<int:purchase_id>', methods=['GET'])
@swag_from({
    'summary': 'Get purchase details',
    'tags': ['User Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'schema': {'type': 'integer'},
            'required': True,
            'description': 'The purchase id'
        }
    ],
    'responses': {
        200: {
            'description': 'A purchase details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'customer': {
                                        'type': 'object',
                                        'properties': {
                                            'customer_id': {'type': 'integer'},
                                            'first_name': {'type': 'string'},
                                            'last_name': {'type': 'string'}
                                        }
                                    },
                                    'purchase_id': {'type': 'integer'},
                                    'purchase_status': {'type': 'string'},
                                    'purchase_vehicle': {
                                        'type': 'object',
                                        'properties': {
                                            'vehicle_id': {'type': 'integer'},
                                            'year': {'type': 'integer'},
                                            'make': {'type': 'string'},
                                            'model': {'type': 'string'},
                                            'vin': {'type': 'string'},
                                            'price': {'type': 'number'}
                                        }
                                    },
                                    'purchase_subtotal': {'type': 'string'},
                                    'tax': {'type': 'number'},
                                    'purchase_total': {'type': 'string'},
                                    'addons': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'addon_id': {'type': 'integer'},
                                                'name': {'type': 'string'},
                                                'price': {'type': 'number'},
                                                'description': {'type': 'string'}
                                            }
                                        }
                                    },
                                    'contracts': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'contract_id': {'type': 'integer'},
                                                'contract_type': {'type': 'string'},
                                                'contract_status': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def get_purchase_details(purchase_id):
    try:
        purchase_dict = g.purchasing_service.get_purchase_details(purchase_id)
        return standardize_response(data=purchase_dict)
    except Exception as e:
        raise e
    
    # def dealer_sign_purchase_contract(self, purchase_id, signature):
    #     '''
    #     Signs a purchase contract
    #     ---
    #     updates contract status to SIGNED
    #     '''
    #     try:
    #         purchase = Purchase.get_purchase(purchase_id)
    #         # check if contract has been signed
    #         if purchase.contract.contract_status != Contract.ContractStatus.CUSTOMER_SIGNED.value:
    #             raise ExposedException('contract has not been signed')
            
    #         # get contract id
    #         contract_id = purchase.contract.contract_id
    #         contract_path = g.contract_service.dealer_sign_contract(contract_id=contract_id, signature=signature)

    #         return contract_path
    #     except Exception as e:
    #         current_app.logger.exception(e)
    #         raise e
    # def get_purchase_contract(self, purchase_id, customer_id):
    #     '''
    #     Retrieves a purchase contract
    #     ---
    #     returns the contract pdf file
    #     '''
    #     try:
    #         purchase = Purchase.get_purchase(purchase_id)
    #         # check if purchase belongs to customer
    #         if purchase.customer_id != customer_id:
    #             raise ExposedException('Unauthorized')
    #         contracts = purchase.contracts
    #         purchase_contract = next((contract for contract in contracts if contract.contract_type == Contract.ContractType.PURCHASE.value), None)
    #         return purchase_contract.contract_path
    #     except Exception as e:
    #         current_app.logger.exception(e)
    #         raise e

# generate purchase contract
@user_bp.route('/purchases/<int:purchase_id>/contract', methods=['POST'])
@swag_from({
    'summary': 'Generate purchase contract',
    'tags': ['User Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'schema': {'type': 'integer'},
            'required': True,
            'description': 'The purchase id'
        }
    ],
    'responses': {
        '200': {
            'description': 'Contract generated successfully',
            'content': {
                'application/pdf': {
                    'schema': { 'type': 'string', 'format': 'binary' }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def generate_purchase_contract(purchase_id):
    try:
        contract_path = g.purchasing_service.generate_purchase_contract(purchase_id)
        return send_file(open(contract_path, 'rb'),
                         mimetype='application/pdf',
                         as_attachment=True,
                         download_name=contract_path.split('/')[-1])
    except Exception as e:
        raise e

# get purchase contract
@user_bp.route('/purchases/<int:purchase_id>/contract', methods=['GET'])
@swag_from({
    'summary': 'Get purchase contract',
    'tags': ['User Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'schema': {'type': 'integer'},
            'required': True,
            'description': 'The purchase id'
        }
    ],
    'responses': {
        '200': {
            'description': 'Contract generated successfully',
            'content': {
                'application/pdf': {
                    'schema': { 'type': 'string', 'format': 'binary' }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def get_purchase_contract(purchase_id):
    try:
        contract_path = g.purchasing_service.get_purchase_contract(purchase_id)
        return send_file(open(contract_path, 'rb'),
                         mimetype='application/pdf',
                         as_attachment=True,
                         download_name=contract_path.split('/')[-1])
    except Exception as e:
        raise e
    
# sign purchase contract
@user_bp.route('/purchases/<int:purchase_id>/contract/sign', methods=['POST'])
@swag_from({
    'summary': 'Sign purchase contract',
    'tags': ['User Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'schema': {'type': 'integer'},
            'required': True,
            'description': 'The purchase id'
        }
    ],
    'requestBody': {
        'description': 'Signature',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'signature': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Contract signed successfully',
            'content': {
                'application/pdf': {
                    'schema': { 'type': 'string', 'format': 'binary' }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def sign_purchase_contract(purchase_id):
    try:
        signature = request.json.get('signature')
        contract_path = g.purchasing_service.dealer_sign_purchase_contract(purchase_id, signature)
        return send_file(open(contract_path, 'rb'),
                         mimetype='application/pdf',
                         as_attachment=True,
                         download_name=contract_path.split('/')[-1])
    except Exception as e:
        raise e