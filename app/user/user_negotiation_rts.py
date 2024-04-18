from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required
from . import user_bp
from app.negotiation.models import Negotiation, Offer
from app.inventory.models import Vehical
from app.exceptions import ExposedException
from app.auth.auth_decorators import manager_required

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# get all negotiations
@user_bp.route('/negotiation/negotiations', methods=['GET'])
@jwt_required()
@manager_required
def get_all_negotiations():
    """
    Get all negotiations
    ---
    tags: [User Negotiation]
    security: [{'BearerAuth': []}]
    responses:
        200:
            description: Negotiations found
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data:
                        type: array
                        items:
                            type: object
                            properties:
                                negotiation_id: { type: integer }
                                vehical:
                                    type: object
                                    properties:
                                        vehical_id: { type: integer }
                                        year: { type: integer }
                                        make: { type: string }
                                        model: { type: string }
                                        image: { type: string }
                                customer_id: { type: integer }
                                negotiation_status: { type: integer }
                                start_date: { type: string }
                                end_date: { type: string }
                    code: { type: integer }
        404:
            description: No negotiations found
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
        500:
            description: Internal server error
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
    """
    try:
        negotiations = g.negotiation_service.get_all_negotiations()
        if negotiations == []:
            return standardize_response(status='fail', message='No negotiations found', data=None, code=404)
        return standardize_response(status='success', message='Negotiations found', 
                                    data=negotiations, code=200)
    except Exception as e:
        raise e
    
# get negotiation details by negotiation id
@user_bp.route('/negotiation/negotiation/<int:negotiation_id>', methods=['GET'])
def get_negotiation_details(negotiation_id):
    """
    Get negotiation details by negotiation id
    ---
    tags: [User Negotiation]
    parameters:
        - in: path
          name: negotiation_id
          required: true
          schema:
            type: integer
    responses:
        200:
            description: Negotiation found
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: 
                        type: object
                        properties:
                            negotiation: 
                                type: object
                                properties:
                                    negotiation_id: { type: integer }
                                    vehical_id: { type: integer }
                                    customer_id: { type: integer }
                                    negotiation_status: { type: integer }
                                    start_date: { type: string }
                                    end_date: { type: string }
                                    offers:
                                        type: array
                                        items:
                                            type: object
                                            properties:
                                                offer_id: { type: integer }
                                                offer_type: { type: string }
                                                offer_price: { type: number }
                                                offer_date: { type: string }
                                                offer_status: { type: string }
                                                message: { type: string }
                            vehicle:
                                type: object
                                properties:
                                    vehical_id: { type: integer }
                                    year: { type: integer }
                                    make: { type: string }
                                    model: { type: string }
                                    image: { type: string }
                    message: { type: string }
                    code: { type: integer }
        404:
            description: Negotiation not found
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
        500:
            description: Internal server error
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
    """
    try:
        negotiation_details = g.negotiation_service.get_negotiation_details(negotiation_id)
        if not negotiation_details:
            return standardize_response(status='fail', message='Negotiation not found', data=None, code=404)
        return standardize_response(status='success', 
                                    message='Negotiation found', 
                                    data=negotiation_details,
                                    code=200)
    except Exception as e:
        raise e

# place counter offer
@user_bp.route('/negotiation/negotiation/<int:negotiation_id>/counter-offer', methods=['POST'])
def place_counter_offer(negotiation_id):
    """
    Place counter offer
    ---
    tags: [User Negotiation]
    parameters:
        - in: path
          name: negotiation_id
          required: true
          schema:
            type: integer
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                offer_price: { type: number }
                message: { type: string }
    responses:
        200:
            description: Counter offer placed
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data:
                        type: object
                        properties:
                            offer_id: { type: integer }
                    code: { type: integer }
        500:
            description: Internal server error
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
    """
    try:
        data = request.get_json()
        offer_price = data.get('offer_price')
        message = data.get('message')
        offer_id = g.negotiation_service.counter_offer(negotiation_id=negotiation_id, offer_price=offer_price,
                                                       message=message)
        return standardize_response(status='success', message='Counter offer placed', data=offer_id, code=200)
    except Exception as e:
        raise e
    
# accept offer
@user_bp.route('/negotiation/negotiation/<int:negotiation_id>/accept-offer', methods=['POST'])
def accept_offer(negotiation_id):
    """
    Accept offer
    ---
    tags: [User Negotiation]
    parameters:
        - in: path
          name: negotiation_id
          required: true
          schema:
            type: integer
    responses:
        200:
            description: Offer accepted
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
        500:
            description: Internal server error
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
    """
    try:
        g.negotiation_service.accept_offer(negotiation_id)
        return standardize_response(status='success', message='Offer accepted', data=None, code=200)
    except Exception as e:
        raise e
    
# reject offer
@user_bp.route('/negotiation/negotiation/<int:negotiation_id>/reject-offer', methods=['POST'])
def reject_offer(negotiation_id):
    """
    Reject offer
    ---
    tags: [User Negotiation]
    parameters:
        - in: path
          name: negotiation_id
          required: true
          schema:
            type: integer
    responses:
        200:
            description: Offer rejected
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
        500:
            description: Internal server error
            schema:
                type: object
                properties:
                    status: { type: string }
                    message: { type: string }
                    data: { type: null }
                    code: { type: integer }
    """
    try:
        g.negotiation_service.reject_offer(negotiation_id)
        return standardize_response(status='success', message='Offer rejected', data=None, code=200)
    except Exception as e:
        raise e