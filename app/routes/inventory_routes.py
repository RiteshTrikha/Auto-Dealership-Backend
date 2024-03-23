from flask import jsonify, request, current_app
from . import routes_bp
from app.services.inventory_service import InventoryService
from app import db
from app.customer.models import Customer

@routes_bp.route('/api/inventory/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from routes_bp!'})

@routes_bp.route('/api/inventory/vehicles', methods=['GET'])
def get_all_vehicles():
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

@routes_bp.route('/api/inventory/vehicle/<vehical_id>', methods=['GET'])
def get_vehicle(vehical_id):
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
    
@routes_bp.route('/api/inventory/top_5_vehicles', methods=['GET'])
def get_top_5_vehicles():
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
    