from flask import jsonify, request, current_app, g
from . import customer_bp
from .models import Customer
from app.negotiation.models import Negotiation, Offer
from app.inventory.models import Vehical
from app.exceptions import ExposedException

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# Place initial offer and create negotiation
@customer_bp.route('/negotiation/negotiation', methods=['POST'])
def create_negotiation():
  """
  Creates a negotiation with customer_id, vehical_id, and offer_price.
  ---
  tags: [Customer Negotiation]
  consumes: [application/json]
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        required: [customer_id, vehical_id, offer_price]
        properties:
          customer_id: {type: integer, description: 'ID of the customer'}
          vehical_id: {type: integer, description: 'ID of the vehical'}
          offer_price: {type: integer, description: 'Offer price'}
          message: {type: string, description: 'customer message'}
  responses:
    201:
      description: Negotiation created
      schema:
        type: object
        properties:
          status: {type: string, description: 'Request status'}
          data: 
            type: object
            properties:
            negotiation_id: {type: integer, description: 'ID of the negotiation'}
          message: {type: string, description: 'Status message'}
          code: {type: integer, description: 'HTTP status code'}

    400:
      description: Bad request
      schema:
        type: object
        properties:
          status: {type: string, description: 'Request status'}
          message: {type: string, description: 'Error message'}
          code: {type: integer, description: 'HTTP status code'}
  """
  try:
      data = request.get_json()
      customer_id = data['customer_id']
      vehical_id = data['vehical_id']
      offer_price = data['offer_price']
      message = data['message']
      negotiation_id = g.negotiation_service.create_negotiation(vehical_id=vehical_id, customer_id=customer_id, 
                                                                offer_price=offer_price, message=message)
      return standardize_response(data={'negotiation_id': negotiation_id}, 
                                  message='Successfully created negotiation',
                                  code=201)
  except Exception as e:
      current_app.logger.error(str(e))
      if isinstance(e, ExposedException):
          return standardize_response(status='fail', message=str(e), code=400)
      return standardize_response(status='fail', message="Error creating negotiation", code=400)

# get list of negotiations by customer
@customer_bp.route('/negotiation/negotiations/<int:customer_id>', methods=['GET'])
def get_negotiations(customer_id):
    """
    Get all negotiations
    ---
    tags: [Customer Negotiation]
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
        description: The id of the customer
    responses:
      200:
        description: Negotiations found
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: 
              type: array
              items:
                type: object
                properties:
                  negotiation_id: {type: integer, description: 'ID of the negotiation'}
                  vehical_id: {type: integer, description: 'ID of the vehical'}
                  customer_id: {type: integer, description: 'ID of the customer'}
                  negotiation_status: {type: integer, description: 'Status of the negotiation'}
                  start_date: {type: string, description: 'Start date of the negotiation'}
                  end_date: {type: string, description: 'End date of the negotiation'}
            message: {type: string, description: 'Status message'}
            code: {type: integer, description: 'HTTP status code'}
      404:
        description: No negotiations found
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: {type: array, description: 'Empty array'}
            message: {type: string, description: 'Status message'}
            code: {type: integer, description: 'HTTP status code'}
      400:
        description: Bad request
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: {type: array, description: 'Empty array'}
            message: {type: string, description: 'Error message'}
            code: {type: integer, description: 'HTTP status code'}
    """
    try:
        negotiations = g.negotiation_service.get_negotiations(customer_id)
        if negotiations == []:
            return standardize_response(status='fail', message='No negotiations found', code=404)
        return standardize_response(data=[negotiation.serialize() for negotiation in negotiations], 
                                    message='Successfully retrieved negotiations')
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error retrieving negotiations", code=400)        

# get negotiation details
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>', methods=['GET'])
def get_negotiation_details(negotiation_id):
    """
    Get negotiation details
    ---
    tags: [Customer Negotiation]
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
    responses:
      200:
        description: Negotiation found
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: 
              type: object
              properties:
                negotiation: 
                  type: object
                  properties:
                    negotiation_id: {type: integer, description: 'ID of the negotiation'}
                    vehical_id: {type: integer, description: 'ID of the vehical'}
                    customer_id: {type: integer, description: 'ID of the customer'}
                    negotiation_status: {type: integer, description: 'Status of the negotiation'}
                    start_date: {type: string, description: 'Start date of the negotiation'}
                    end_date: {type: string, description: 'End date of the negotiation'}
                offers: 
                  type: array
                  items:
                    type: object
                    properties:
                      offer_id: {type: integer, description: 'ID of the offer'}
                      negotiation_id: {type: integer, description: 'ID of the negotiation'}
                      offer_price: {type: integer, description: 'Offer price'}
                      offer_status: {type: integer, description: 'Status of the offer'}
            message: {type: string, description: 'Status message'}
            code: {type: integer, description: 'HTTP status code'}
      404:
        description: No negotiation found
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: {type: object, description: 'Empty object'}
            message: {type: string, description: 'Status message'}
            code: {type: integer, description: 'HTTP status code'}
      400:
        description: Bad request
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: {type: object, description: 'Empty object'}
            message: {type: string, description: 'Error message'}
            code: {type: integer, description: 'HTTP status code'}
    """
    try:
        negotiation, offers = g.negotiation_service.get_negotiation_details(negotiation_id)
        if negotiation is None:
            return standardize_response(status='fail', message='No negotiation found', code=404)
        return standardize_response(data={'negotiation': negotiation.serialize(),
                                        'offers': [offer.serialize() for offer in offers]}, 
                                    message='Successfully retrieved negotiation')
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error retrieving negotiation", code=400)

# place additional offer
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/offer', methods=['POST'])
def place_offer(negotiation_id):
    """
    Place additional offer
    ---
    tags: [Customer Negotiation]
    consumes: [application/json]
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [offer_price]
          properties:
            offer_price: {type: integer, description: 'Offer price'}
            message: {type: string, description: 'customer message'}
    responses:
      201:
        description: Offer placed
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: 
              type: object
              properties:
                offer_id: {type: integer, description: 'ID of the offer'}
            message: {type: string, description: 'Status message'}
            code: {type: integer, description: 'HTTP status code'}
      400:
        description: Bad request
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            message: {type: string, description: 'Error message'}
            code: {type: integer, description: 'HTTP status code'}
    """
    try:
        data = request.get_json()
        offer_price = data['offer_price']
        message = data['message']
        offer_id = g.negotiation_service.place_offer(negotiation_id=negotiation_id, offer_price=offer_price,
                                                    message=message)
        return standardize_response(data={'offer_id': offer_id}, 
                                    message='Successfully placed offer', 
                                    code=201)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error placing offer", code=400)

# accept counter offer
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/accept', methods=['POST'])
def accept_offer(negotiation_id):
    """
    Accept an offer
    ---
    tags: [Customer Negotiation]
    consumes: [application/json]
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
    responses:
      200:
        description: Offer accepted
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: {type: object, description: 'Empty object'}
            message: {type: string, description: 'Status message'}
            code: {type: integer, description: 'HTTP status code'}
      400:
        description: Bad request
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            message: {type: string, description: 'Error message'}
            code: {type: integer, description: 'HTTP status code'}
    """
    try:
        g.negotiation_service.accept_counter_offer(negotiation_id)
        return standardize_response(message='Successfully accepted offer')
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message="Error accepting offer", code=400)
    
# reject counter offer
@customer_bp.route('/negotiation/negotiation/<int:negotiation_id>/reject', methods=['POST'])
def reject_offer(negotiation_id):
    """
    Reject an offer
    ---
    tags: [Customer Negotiation]
    consumes: [application/json]
    parameters:
      - in: path
        name: negotiation_id
        type: integer
        required: true
        description: The id of the negotiation
    responses:
      200:
        description: Offer rejected
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            data: {type: object, description: 'Empty object'}
            message: {type: string, description: 'Status message'}
            code: {type: integer, description: 'HTTP status code'}
      400:
        description: Bad request
        schema:
          type: object
          properties:
            status: {type: string, description: 'Request status'}
            message: {type: string, description: 'Error message'}
            code: {type: integer, description: 'HTTP status code'}
    """
    try:
        g.negotiation_service.reject_counter_offer(negotiation_id)
        return standardize_response(message='Successfully rejected offer')
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error rejecting offer", code=400)