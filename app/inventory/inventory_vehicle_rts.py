from flask import request
from flasgger import swag_from
from . import inventory_bp
from .services import InventoryService

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response


# get all vehicles
@inventory_bp.route('/vehicles', methods=['GET'])
@swag_from(
    {
        'summary': 'Get all vehicles',
        'tags': ['Vehicle'],
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
                'description': 'Number of vehicles per page'
            },
            {
                'in': 'query',
                'name': 'query',
                'schema': { 'type': 'array',
                            'items': { 'type': 'string' } }
                            ,
                'description': 'Search query'
            }
        ],
        'responses': {
            200: {
                'description': 'A list of vehicles',
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
                                        'vehicles': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'vehicle_id': { 'type': 'integer' },
                                                    'price': { 'type': 'integer' },
                                                    'year': { 'type': 'string' },
                                                    'make': { 'type': 'string' },
                                                    'model': { 'type': 'string' },
                                                    'body_type': { 'type': 'string' },
                                                    'miles': { 'type': 'integer' },
                                                    'mpg': { 'type': 'integer' },
                                                    'color': { 'type': 'string' },
                                                    'fuel_type': { 'type': 'string' },
                                                    'transmission': { 'type': 'string' },
                                                    'image': { 'type': 'string' },
                                                    'vehicle_status': { 'type': 'integer' }
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
                'description': 'No vehicles found',
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
                'description': 'Failed to retrieve vehicles',
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
def get_vehicles():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        queries = request.args.getlist('query')
        vehicles_dict = InventoryService().get_vehicles(page=page, limit=limit, queries=queries)
        return standardize_response(status='success', data=vehicles_dict, 
                                    message='Successfully retrieved vehicles', code=200)
    except Exception as e:
        raise e
        

# get vehicle by id
@inventory_bp.route('/vehicle/<vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """
    Get vehicle by id
    ---
    tags: [Vehicle]
    parameters:
        - in: path
          name: vehicle_id
          schema:
            type: integer
          required: true
          description: Vehicle id
    responses:
        200:
            description: A vehicle
            schema:
                type: object
                properties:
                    status: { type: string }
                    data: 
                        type: object
                        properties:
                            vehicle_id: { type: integer }
                            vin: { type: string }
                            price: { type: integer }
                            year: { type: string }
                            make: { type: string }
                            model: { type: string }
                            body_type: { type: string }
                            miles: { type: integer }
                            mpg: { type: integer }
                            color: { type: string }
                            fuel_type: { type: string }
                            transmission: { type: string }
                            image: { type: string }
                            vehicle_status: { type: integer }
                    message: { type: string }
                    code: { type: integer }
        404:
            description: Vehicle not found
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    code: { type: integer }
        500:
            description: Failed to retrieve vehicle
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
        vehicle = InventoryService().get_vehicle(vehicle_id)
        return standardize_response(status='success', data=vehicle,
                                     message='Successfully retrieved vehicle', code=200)
    except Exception as e:
        raise e


# get top 5 vehicles
@inventory_bp.route('/top-vehicles', methods=['GET'])
def get_top_5_vehicles():
    """
    Get top 5 vehicles
    ---
    tags:
      - Vehicle
    responses:
      200:
        description: A list of top 5 vehicles
        schema:
          type: object
          properties:
            status: {type: string}
            data:
              type: array
              items:
                type: object
                properties:
                  vehicle_id: {type: integer}
                  price: {type: integer}
                  year: {type: string}
                  make: {type: string}
                  model: {type: string}
                  body_type: {type: string}
                  miles: {type: integer}
                  mpg: {type: integer}
                  color: {type: string}
                  fuel_type: {type: string}
                  transmission: {type: string}
                  image: {type: string}
                  vehicle_status: {type: integer}
            message:
              type: string
            code:
              type: integer
        404:
            description: No vehicles found
            schema:
                type: object
                properties:
                status: {type: string}
                message: {type: string}
                code: {type: integer}
        500:
            description: Failed to retrieve top vehicles
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
        vehicles = InventoryService().get_top_5_vehicles()
        return standardize_response(status='success', data=vehicles, 
                                    message='Successfully retrieved top vehicles', code=200)
    except Exception as e:
        raise e