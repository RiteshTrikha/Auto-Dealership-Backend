from flask import jsonify, request, current_app, g
from . import inventory_bp
from app import g
from .services import InventoryService
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# get all vehicles
@inventory_bp.route('/inventory/vehicles', methods=['GET'])
def get_all_vehicles():
    """
    Get all vehicles
    ---
    tags:
      - Vehicle
    responses:
      200:
        description: A list of vehicles
        content:
          application/json:
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
                      miles: {type: integer}
                      mpg: {type: integer}
                      color: {type: string}
                      fuel_type: {type: string}
                      transmission: {type: string}
                      image: {type: string}
                      vehicle_status: {type: integer}
                message: {type: string}
                code: {type: integer}
        404:
            description: No vehicles found
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
        vehicles = InventoryService().get_all_vehicles()
        return standardize_response(status='success', data=vehicles, 
                                    message='Successfully retrieved vehicles', code=200)
    except Exception as e:
        raise e
        

# get vehicle by id
@inventory_bp.route('/inventory/vehicle/<vehical_id>', methods=['GET'])
def get_vehicle(vehical_id):
    """
    Get vehicle by id
    ---
    tags: [Vehicle]
    parameters:
        - in: path
          name: vehical_id
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
        vehicle = InventoryService().get_vehicle(vehical_id)
        return standardize_response(status='success', data=vehicle,
                                     message='Successfully retrieved vehicle', code=200)
    except Exception as e:
        raise e

# get top 5 vehicles
@inventory_bp.route('/inventory/top-vehicles', methods=['GET'])
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