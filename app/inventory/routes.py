from flask import jsonify, request
from . import inventory_bp
from app import g
from .services import InventoryService

@inventory_bp.route('/api/inventory/vehicles', methods=['GET'])
def get_all_vehicles():
    """
    Get all vehicles
    ---
    tags:
      - Inventory
    """
    try:
        vehicles = InventoryService().get_all_vehicles()
        if vehicles is None:
            return jsonify(
                status='fail', 
                data=[], 
                message='No vehicles found'
                ), 404
        return jsonify(
            status='success', 
            data=[vehicle.serialize() for vehicle in vehicles], 
            message='Successfully retrieved all vehicles'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail', 
            data=[], 
            message=str(e)
            ), 400

@inventory_bp.route('/api/inventory/vehicle/<vehical_id>', methods=['GET'])
def get_vehicle(vehical_id):
    """
    Get a vehicle by id
    ---
    tags:
      - Inventory
    parameters:
        - name: vehical_id
          in: path
          type: integer
          required: true
          description: The ID of the vehicle
    """
    try:
        vehicle = InventoryService().get_vehicle(vehical_id)
        if vehicle is None:
            return jsonify(
                status='fail', 
                data=[], 
                message='Vehicle not found'
                ), 404
        return jsonify(
            status='success', 
            data=vehicle.serialize(), 
            message='Successfully retrieved vehicle'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail', 
            data=[], 
            message=str(e)
            ), 400
    
@inventory_bp.route('/api/inventory/top_5_vehicles', methods=['GET'])
def get_top_5_vehicles():
    """
    Get top 5 vehicles
    ---
    tags:
      - Inventory
    """
    try:
        vehicles = InventoryService().get_top_5_vehicles()
        if vehicles is None:
            return jsonify(
                status='fail', 
                data=[], 
                message='No vehicles found'
                ), 404
        return jsonify(
            status='success', 
            data=[vehicle.serialize() for vehicle in vehicles], 
            message='Successfully retrieved top 5 vehicles'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail', 
            data=[], 
            message=str(e)
            ), 400
    