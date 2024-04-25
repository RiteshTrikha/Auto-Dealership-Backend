from flask import jsonify, request, g, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import customer_bp
from flasgger import swag_from
from .models import Customer
from app.purchasing.models import Purchase, Purchasevehicle, PurchaseAddon, Finance, Payment
from app.contracts.models import Contract

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# initiate car purchase
@customer_bp.route('/purchase', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Initiate car purchase',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'description': 'Negotiation id',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': { 'negotiation_id': { 'type': 'integer' } },
                    'required': [ 'negotiation_id' ]
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Purchase initiated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'purchase_id': { 'type': 'integer' },
                                    'purchase_status': { 'type': 'string' },
                                    'purchase_date': { 'type': 'string' }
                                }
                            },
                            'message': { 'type': 'string' }
                        }
                    }
                }
            }
        }
    }
})
def initiate_car_purchase():
    try:
        customer_id = get_jwt_identity().get('customer_id')
        data = request.get_json()
        negotiation_id = data.get('negotiation_id')
        current_app.logger.info(f'customer_id: {customer_id}, negotiation_id: {negotiation_id}')
        purchase_dict = g.purchasing_service.initiate_car_purchase(customer_id=customer_id, 
                                                                   negotiation_id=negotiation_id)
        return standardize_response(data=purchase_dict, message='Purchase initiated successfully')
    except Exception as e:
        raise e
    
# get purchases
@customer_bp.route('/purchases', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get all purchases',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {
            'description': 'Purchases retrieved successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'purchases': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'purchase_id': { 'type': 'integer' },
                                                'purchase_status': { 'type': 'string' },
                                                'purchase_type': { 'type': 'string' },
                                                'purchase_vehicle': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'vehicle_id': { 'type': 'integer' },
                                                        'year': { 'type': 'integer' },
                                                        'make': { 'type': 'string' },
                                                        'model': { 'type': 'string' }
                                                    }
                                                },
                                                'purchase_total': { 'type': 'number' }
                                            }
                                        }
                                    }
                                }
                            },
                            'message': { 'type': 'string' }
                        }
                    }
                }
            }
        }
    }
})
def get_customer_purchases():
    try:
        customer_id = get_jwt_identity().get('customer_id')
        purchases_dict = g.purchasing_service.get_customer_purchases(customer_id)
        return standardize_response(data=purchases_dict, message='Purchases retrieved successfully')
    except Exception as e:
        raise e
    
# get purchase details
@customer_bp.route('/purchase/<int:purchase_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get purchase details',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'required': True,
            'description': 'Purchase id',
            'schema': { 'type': 'integer' }
        }
    ],
    'responses': {
        '200': {
            'description': 'Purchase details retrieved successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'purchase_id': { 'type': 'integer' },
                                    'purchase_status': { 'type': 'string' },
                                    'purchase_type': { 'type': 'string' },
                                    'purchase_vehicle': {
                                        'type': 'object',
                                        'properties': {
                                            'vehicle_id': { 'type': 'integer' },
                                            'year': { 'type': 'integer' },
                                            'make': { 'type': 'string' },
                                            'model': { 'type': 'string' },
                                            'vin': { 'type': 'string' },
                                            'price': { 'type': 'number' }
                                        }
                                    },
                                    'purchase_subtotal': { 'type': 'number' },
                                    'tax': { 'type': 'number' },
                                    'purchase_total': { 'type': 'number' },
                                    'addons': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'addon_id': { 'type': 'integer' },
                                                'addon_name': { 'type': 'string' },
                                                'addon_price': { 'type': 'number' },
                                                'addon_description': { 'type': 'string' }
                                            }
                                        }
                                    },
                                    'contract': {
                                        'type': 'object',
                                        'properties': {
                                            'contract_id': { 'type': 'integer' },
                                            'contract_status': { 'type': 'string' },
                                            'contract_type': { 'type': 'string' },
                                            'contract_date': { 'type': 'string' }
                                        }
                                    },
                                    'payment': {
                                        'type': 'object',
                                        'properties': {
                                            'payment_id': { 'type': 'integer' },
                                            'payment_status': { 'type': 'string' },
                                            'payment_date': { 'type': 'string' },
                                            'payment_amount': { 'type': 'number' }
                                        }
                                    }
                                }
                            },
                            'message': { 'type': 'string' }
                        }
                    }
                }
            }
        }
    }
})
def get_customer_purchase_details(purchase_id):
    try:
        customer_id = get_jwt_identity().get('customer_id')
        purchase_dict = g.purchasing_service.get_customer_purchase_details(customer_id, purchase_id)
        return standardize_response(data=purchase_dict, message='Purchase details retrieved successfully')
    except Exception as e:
        raise e

# add addons to purchase
@customer_bp.route('/purchase/<int:purchase_id>/addons', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Add addons to purchase',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'required': True,
            'description': 'Purchase id',
            'schema': { 'type': 'integer' }
        }
    ],
    'requestBody': {
        'description': 'Addon ids',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': { 'addon_ids': { 'type': 'array', 'items': { 'type': 'integer' } } },
                    'required': [ 'addon_ids' ]
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Addons added successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'purchase_id': { 'type': 'integer' },
                                    'addons': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'addon_id': { 'type': 'integer' },
                                                'addon_name': { 'type': 'string' },
                                                'addon_price': { 'type': 'number' },
                                                'addon_description': { 'type': 'string' }
                                            }
                                        }
                                    }
                                }
                            },
                            'message': { 'type': 'string' }
                        }
                    }
                }
            }
        }
    }
})
def add_addons_to_purchase(purchase_id):
    try:
        customer_id = get_jwt_identity().get('customer_id')
        data = request.get_json()
        addon_ids = data.get('addon_ids')
        purchase_addons_dict = g.purchasing_service.add_addons_to_purchase(customer_id, purchase_id, addon_ids)
        return standardize_response(data=purchase_addons_dict, message='Addons added successfully')
    except Exception as e:
        raise e
    
# TODO: add route to finance purchase

# generate contract
@customer_bp.route('/purchase/<int:purchase_id>/contract', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Generate purchase contract',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'required': True,
            'description': 'Purchase id',
            'schema': { 'type': 'integer' }
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
def generate_customer_purchase_contract(purchase_id):
    try:
        customer_id = get_jwt_identity().get('customer_id')
        contract_path = g.purchasing_service.generate_customer_purchase_contract(purchase_id, customer_id)
        current_app.logger.info(f'contract_path: {contract_path}')
        return send_file(open(contract_path, 'rb'),
                            mimetype='application/pdf',
                            as_attachment=True,
                            download_name=contract_path.split('/')[-1])
    except Exception as e:
        raise e

# get contract
@customer_bp.route('/purchase/<int:purchase_id>/contract', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get purchase contract',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'required': True,
            'description': 'Purchase id',
            'schema': { 'type': 'integer' }
        }
    ],
    'responses': {
        '200': {
            'description': 'Contract retrieved successfully',
            'content': {
                'application/pdf': {
                    'schema': { 'type': 'string', 'format': 'binary' }
                }
            }
        }
    }
})
def get_customer_purchase_contract(purchase_id):
    try:
        customer_id = get_jwt_identity().get('customer_id')
        contract_path = g.purchasing_service.get_customer_purchase_contract(purchase_id=purchase_id, 
                                                                   customer_id=customer_id)
        return send_file(open(contract_path, 'rb'),
                            mimetype='application/pdf',
                            as_attachment=True,
                            download_name=contract_path.split('/')[-1])
    except Exception as e:
        raise e

# sign contract
@customer_bp.route('/purchase/<int:purchase_id>/contract/sign', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Sign purchase contract',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'required': True,
            'description': 'Purchase id',
            'schema': { 'type': 'integer' }
        }
    ],
    'requestBody': {
        'description': 'Signature',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': { 'signature': { 'type': 'string' } },
                    'required': [ 'signature' ]
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
def sign_purchase_contract(purchase_id):
    try:
        customer_id = get_jwt_identity().get('customer_id')
        data = request.get_json()
        signature = data.get('signature')
        contract_path = g.purchasing_service.customer_sign_purchase_contract(purchase_id=purchase_id,
                                                                            customer_id=customer_id,
                                                                            signature=signature)
        return send_file(open(contract_path, 'rb'),
                            mimetype='application/pdf',
                            as_attachment=True,
                            download_name=contract_path.split('/')[-1])
    except Exception as e:
        raise e
    
# pay purchase ACH
@customer_bp.route('/purchase/<int:purchase_id>/payment', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Pay for purchase',
    'tags': ['Customer Purchasing'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'purchase_id',
            'required': True,
            'description': 'Purchase id',
            'schema': { 'type': 'integer' }
        }
    ],
    'requestBody': {
        'description': 'Payment details',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'account_number': { 'type': 'string' },
                        'routing_number': { 'type': 'string' }
                    },
                    'required': [ 'payment_method', 'payment_amount' ]
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Payment successful',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'payment_id': { 'type': 'integer' },
                                    'payment_status': { 'type': 'string' },
                                    'payment_date': { 'type': 'string' },
                                    'payment_amount': { 'type': 'number' }
                                }
                            },
                            'message': { 'type': 'string' }
                        }
                    }
                }
            }
        }
    }
})
def pay_purchase_ACH(purchase_id):
    try:
        customer_id = get_jwt_identity().get('customer_id')
        account_number = request.json.get('account_number')
        routing_number = request.json.get('routing_number')
        payment_dict = g.purchasing_service.pay_purchase_ACH(purchase_id=purchase_id, customer_id=customer_id,
                                                             account_number=account_number, routing_number=routing_number)
        return standardize_response(data=payment_dict, message='Payment successful')
    except Exception as e:
        raise e