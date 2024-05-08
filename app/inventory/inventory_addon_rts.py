from flask import request
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from . import inventory_bp
from app.auth.auth_decorators import user_required, manager_required
from .services import InventoryService  # Ensure your service layer is correctly imported
inventory_service = InventoryService()

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response


@inventory_bp.route('/addons', methods=['GET'])
@swag_from({
    'summary': 'Get all addons',
    'description': 'Retrieve a list of all available addons',
    'tags': ['Addons'],
    'responses': {
        200: {
            'description': 'All addons retrieved successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'addon_id': {'type': 'integer'},
                                'addon_name': {'type': 'string'},
                                'price': {'type': 'integer'},
                                'description': {'type': 'string'},
                                'status': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        },
        400: {'description': 'Bad request'},
        500: {'description': 'Internal server error'}
    }
})
def get_all_addons():
    try:
        addons = inventory_service.get_addons()
        return standardize_response(data=addons)
    except Exception as e:
        return e

# Ensure to register the blueprint in your main app configuration
