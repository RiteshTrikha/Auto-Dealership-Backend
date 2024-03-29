from flask import jsonify, request
from . import customer_bp
from app import g
from .models import Customer
from app.negotiation.models import Negotiation, Offer
from app.inventory.models import Vehical

# test routes

# @customer_bp.route('/api/customer/hello', methods=['GET'])
# def hello():
#     return jsonify({'message': 'Hello from customer_bp!'})

# @customer_bp.route('/api/customer/<int:customer_id>', methods=['GET'])
# def get_customer(customer_id):
#     customer = db.session.query(Customer).filter(Customer.customer_id == customer_id).first()
#     if customer:
#         return jsonify(customer.serialize())
#     else:
#         return jsonify({'message': 'Customer not found'}), 404
    
# negotiation routes

@customer_bp.route('/api/negotiation/negotiation', methods=['POST'])
def create_negotiation():
    """
    Create a negotiation for a vehicle and place initial offer
    ---
    tags:
      - Negotiation
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: Required parameters for creating a negotiation
        required: true
        schema:
          type: object
          required:
            - vehical_id
            - customer_id
            - offer_price
          properties:
            vehical_id:
              type: integer
              description: The id of the vehicle
            customer_id:
              type: integer
              description: The id of the customer
            offer_price:
              type: number
              format: float
              description: The initial offer price
    responses:
      201:
        description: Successfully created negotiation
        schema:
          type: object
          properties:
            status:
              type: string
              description: The status of the request
            data:
              type: object
              properties:
                negotiation_id:
                  type: integer
                  description: The id of the negotiation
            message:
              type: string
              description: A message indicating the status of the request
      400:
        description: Bad request
        schema:
          type: object
          properties:
            status:
              type: string
              description: The status of the request
            data:
              type: object
            message:
              type: string
              description: A message indicating the status of the request
    """
    try:
        data = request.get_json()
        vehical_id = data['vehical_id']
        customer_id = data['customer_id']
        offer_price = data['offer_price']
        negotiation_id = g.negotiation_service.create_negotiation(vehical_id, customer_id, offer_price)
        return jsonify(
            status='success', 
            data={'negotiation_id': negotiation_id}, 
            message='Successfully created negotiation'
            ), 201
    except Exception as e:
        return jsonify(
            status='fail', 
            data={}, 
            message=str(e)
            ), 400

@customer_bp.route('/api/negotiation/negotiations', methods=['GET'])
def get_all_negotiations():
    """
    Get all negotiations
    ---
    tags:
      - Negotiation
    responses:
      200:
        description: Successfully retrieved all negotiations
        schema:
          type: object
          properties:
            status:
              type: string
              description: The status of the request
            data:
              type: array
              items:
                type: object
                properties:
                  negotiation_id:
                    type: integer
                    description: The id of the negotiation
                  customer_id:
                    type: integer
                    description: The id of the customer
                  negotiation_status:
                    type: integer
                    description: The status of the negotiation
                  start_date:
                    type: string
                    description: The start date of the negotiation
                  end_date:
                    type: string
                    description: The end date of the negotiation
            message:
              type: string
              description: A message indicating the status of the request
      404:
        description: No negotiations found
        schema:
          type: object
          properties:
            status:
              type: string
              description: The status of the request
            data:
              type: array
            message:
              type: string
              description: A message indicating the status of the request
      400:
        description: Bad request
        schema:
          type: object
          properties:
            status:
              type: string
              description: The status of the request
            data:
              type: array
            message:
              type: string
              description: A message indicating the status of the request
    """
    try:
        negotiations = g.negotiation_service.get_all_negotiations()
        if negotiations is None:
            return jsonify(
                status='fail', 
                data=[], 
                message='No negotiations found'
                ), 404
        return jsonify(
            status='success', 
            data=[negotiation.serialize() for negotiation in negotiations], 
            message='Successfully retrieved all negotiations'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail', 
            data=[], 
            message=str(e)
            ), 400

@customer_bp.route('/api/negotiation/negotiations/<int:customer_id>', methods=['GET'])
def get_negotiations(customer_id):
    """
    Get negotiations for a customer
    ---
    tags:
      - Negotiation
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
        description: The id of the customer
    """
    try:
        negotiations = g.negotiation_service.get_negotiations(customer_id)
        if negotiations is None:
            return jsonify(
                status='fail', 
                data=[], 
                message='No negotiations found'
                ), 404
        return jsonify(
            status='success', 
            data=[negotiation.serialize() for negotiation in negotiations], 
            message='Successfully retrieved negotiations'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail', 
            data=[], 
            message=str(e)
            ), 400

@customer_bp.route('/api/negotiation/negotiation/<int:negotiation_id>', methods=['GET'])
def get_negotiation_details(negotiation_id):
    """
    Get negotiation details
    ---
    tags:
      - Negotiation
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
    """
    try:
        negotiation, offers = g.negotiation_service.get_negotiation_details(negotiation_id)
        if negotiation is None:
            return jsonify(
                status='fail', 
                data={}, 
                message='No negotiation found'
                ), 404
        return jsonify(
            status='success', 
            data={
                'negotiation': negotiation.serialize(), 
                'offers': [offer.serialize() for offer in offers]
                },
            message='Successfully retrieved negotiation'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail', 
            data={}, 
            message=str(e)
            ), 400
    
@customer_bp.route('/api/negotiation/negotiation/<int:negotiation_id>/counter', methods=['POST'])
def counter_offer(negotiation_id):
    """
    Counter offer for a negotiation
    ---
    tags:
      - Negotiation
    consumes:
      - application/json
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
      - in: body
        name: body
        description: Required parameters for countering an offer
        required: true
        schema:
          type: object
          required:
            - offer_price
          properties:
            offer_price:
              type: number
              format: float
              description: The counter offer price
    """
    try:
        data = request.get_json()
        offer_price = data['offer_price']
        offer_id = g.negotiation_service.counter_offer(negotiation_id, offer_price)
        if offer_id is None:
            return jsonify(
                status='fail', 
                data={}, 
                message='No negotiation found'
                ), 404
        return jsonify(
            status='success', 
            data={'offer_id': offer_id}, 
            message='Successfully countered offer'
            ), 201
    except Exception as e:
        return jsonify(
            status='fail', 
            data={}, 
            message=str(e)
            ), 400
    
@customer_bp.route('/api/negotiation/negotiation/<int:negotiation_id>/offer', methods=['POST'])
def additional_offer(negotiation_id):
    """
    Additional offer for a negotiation
    ---
    tags:
      - Negotiation
    consumes:
      - application/json
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
      - in: body
        name: body
        description: Required parameters for placing an additional offer
        required: true
        schema:
          type: object
          required:
            - offer_price
          properties:
            offer_price:
              type: number
              format: float
              description: The additional offer price
    """
    try:
        data = request.get_json()
        offer_price = data['offer_price']
        offer_id = g.negotiation_service.additional_offer(negotiation_id, offer_price)
        if offer_id is None:
            return jsonify(
                status='fail', 
                data={}, 
                message='No negotiation found'
                ), 404
        return jsonify(
            status='success', 
            data={'offer_id': offer_id}, 
            message='Successfully placed additional offer'
            ), 201
    except Exception as e:
        return jsonify(
            status='fail', 
            data={}, 
            message=str(e)
            ), 400
    
  #accept offer
@customer_bp.route('/api/negotiation/negotiation/<int:negotiation_id>/accept', methods=['POST'])
def accept_offer(negotiation_id):
    """
    Accept an offer
    ---
    tags:
      - Negotiation
    consumes:
      - application/json
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
    """
    try:
        g.negotiation_service.accept_offer(negotiation_id)
        return jsonify(
            status='success', 
            data={}, 
            message='Successfully accepted offer'
            ), 201
    except Exception as e:
        return jsonify(
            status='fail', 
            data={}, 
            message=str(e)
            ), 400
    
@customer_bp.route('/api/negotiation/negotiation/<int:negotiation_id>/reject', methods=['POST'])
def reject_offer(negotiation_id):
    """
    Reject an offer
    ---
    tags:
      - Negotiation
    consumes:
      - application/json
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
    """
    try:
        g.negotiation_service.reject_offer(negotiation_id)
        return jsonify(
            status='success', 
            data={}, 
            message='Successfully rejected offer'
            ), 201
    except Exception as e:
        return jsonify(
            status='fail', 
            data={}, 
            message=str(e)
            ), 400