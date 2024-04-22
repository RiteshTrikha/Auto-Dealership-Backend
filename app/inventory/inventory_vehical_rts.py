from flask import request
from flasgger import swag_from
from . import inventory_bp
from .services import InventoryService

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# get all vehicals
@inventory_bp.route('/vehicals', methods=['GET'])
@swag_from(
    {
        'summary': 'Get all vehicals',
        'tags': ['vehical'],
        'parameters': [
            {
                'in': 'query',
                'name': 'page',
                'schema': { 'type': 'integer' },
                'description': 'Page number'
            },
            {
                'in': 'query',
                'name': 'limit',
                'schema': { 'type': 'integer' },
                'description': 'Number of vehicals per page'
            },
            {
                'in': 'query',
                'name': 'query',
                'schema': { 'type': 'string' },
                'description': 'Search query'
            }
        ],
        'responses': {
            200: {
                'description': 'A list of vehicals',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': { 'type': 'string' },
                                'data': {
                                    'type': 'object',
                                    'properties': {
                                        'num_of_pages': { 'type': 'integer' },
                                        'num_of_results': { 'type': 'integer' },
                                        'page': { 'type': 'integer' },
                                        'vehicals': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'vehical_id': { 'type': 'integer' },
                                                    'price': { 'type': 'integer' },
                                                    'year': { 'type': 'string' },
                                                    'make': { 'type': 'string' },
                                                    'model': { 'type': 'string' },
                                                    'miles': { 'type': 'integer' },
                                                    'mpg': { 'type': 'integer' },
                                                    'color': { 'type': 'string' },
                                                    'fuel_type': { 'type': 'string' },
                                                    'transmission': { 'type': 'string' },
                                                    'image': { 'type': 'string' },
                                                    'vehical_status': { 'type': 'integer' }
                                                }
                                            }
                                        }
                                    }
                                },
                                'message': { 'type': 'string' },
                                'code': { 'type': 'integer' }
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'No vehicals found',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': { 'type': 'string' },
                                'message': { 'type': 'string' },
                                'code': { 'type': 'integer' }
                            }
                        }
                    }
                }
            },
            500: {
                'description': 'Failed to retrieve vehicals',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': { 'type': 'string' },
                                'message': { 'type': 'string' },
                                'code': { 'type': 'integer' }
                            }
                        }
                    }
                }
            },
            400: {
                'description': 'Bad request',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': { 'type': 'string' },
                                'message': { 'type': 'string' },
                                'code': { 'type': 'integer' }
                            }
                        }
                    }
                }
            }
        }
    })
def get_vehicals():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        query = request.args.get('query', None, type=str)
        vehicals_dict = InventoryService().get_vehicals(page=page, limit=limit, query=query)
        return standardize_response(status='success', data=vehicals_dict, 
                                    message='Successfully retrieved vehicals', code=200)
    except Exception as e:
        raise e
        

# get vehical by id
@inventory_bp.route('/vehical/<vehical_id>', methods=['GET'])
def get_vehical(vehical_id):
    """
    Get vehical by id
    ---
    tags: [vehical]
    parameters:
        - in: path
          name: vehical_id
          schema:
            type: integer
          required: true
          description: vehical id
    responses:
        200:
            description: A vehical
            schema:
                type: object
                properties:
                    status: { type: string }
                    data: 
                        type: object
                        properties:
                            vehical_id: { type: integer }
                            vin: { type: string }
                            price: { type: integer }
                            year: { type: string }
                            make: { type: string }
                            model: { type: string }
                            miles: { type: integer }
                            mpg: { type: integer }
                            color: { type: string }
                            fuel_type: { type: string }
                            transmission: { type: string }
                            image: { type: string }
                            vehical_status: { type: integer }
                    message: { type: string }
                    code: { type: integer }
        404:
            description: vehical not found
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    code: { type: integer }
        500:
            description: Failed to retrieve vehical
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    code: { type: integer }
        400:
            description: Bad request
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    code: { type: integer }
    """
    try:
        vehical = InventoryService().get_vehical(vehical_id)
        return standardize_response(status='success', data=vehical,
                                     message='Successfully retrieved vehical', code=200)
    except Exception as e:
        raise e

# get top 5 vehicals
@inventory_bp.route('/top-vehicals', methods=['GET'])
def get_top_5_vehicals():
    """
    Get top 5 vehicals
    ---
    tags:
      - vehical
    responses:
      200:
        description: A list of top 5 vehicals
        schema:
          type: object
          properties:
            status: {type: string}
            data:
              type: array
              items:
                type: object
                properties:
                  vehical_id: {type: integer}
                  price: {type: integer}
                  year: {type: string}
                  make: {type: string}
                  model: {type: string}
                  miles: {type: integer}
                  mpg: {type: integer}
                  color: {type: string}
                  fuel_type: {type: string}
                  transmission: {type: string}
                  image: {type: string}
                  vehical_status: {type: integer}
            message:
              type: string
            code:
              type: integer
        404:
            description: No vehicals found
            schema:
                type: object
                properties:
                status: {type: string}
                message: {type: string}
                code: {type: integer}
        500:
            description: Failed to retrieve top vehicals
            schema:
                type: object
                properties:
                status: {type: string}
                message: {type: string}
                code: {type: integer}
        400:
            description: Bad request
            schema:
                type: object
                properties:
                status: {type: string}
                message: {type: string}
                code: {type: integer}
    """
    try:
        vehicals = InventoryService().get_top_5_vehicals()
        return standardize_response(status='success', data=vehicals, 
                                    message='Successfully retrieved top vehicals', code=200)
    except Exception as e:
        raise e