from flask_restx import Namespace, Resource
from flask import current_app
from ..models.negotiation_models import negotiation_model, negotiation_details_model, offer_model, create_negotiation_model
# import services
from app.negotiation.services import NegotiationService
# import utilities
from app.api.utilities import Utilities
standardize_response = Utilities().standardize_response

customer_negotiation_ns = Namespace('CustomerNegotiation', description='Customer Negotiation related operations')

# register models with namespace
customer_negotiation_ns.models[negotiation_model.name] = negotiation_model
customer_negotiation_ns.models[offer_model.name] = offer_model
customer_negotiation_ns.models[negotiation_details_model.name] = negotiation_details_model
customer_negotiation_ns.models[create_negotiation_model.name] = create_negotiation_model

# routes

# place initial offer and create negotiation
@customer_negotiation_ns.route('/negotiation')
class CustomerNegotiation(Resource):
    @customer_negotiation_ns.expect(create_negotiation_model, validate=True)
    @customer_negotiation_ns.marshal_with(offer_model)
    def post(self):
        '''Place initial offer and create negotiation'''
        try:
            data = customer_negotiation_ns.payload
            vehicle_id = data['vehicle_id']
            customer_id = data['customer_id']
            offer_price = data['offer_price']
            negotiation_id = NegotiationService.create_negotiation(vehicle_id, customer_id, offer_price)
            return standardize_response(
                status='success',
                data={'negotiation_id': negotiation_id},
                code=201
            )
        except Exception as e:
            current_app.logger.error(e)
            return standardize_response(
                status='fail',
                message='Failed to create negotiation',
                code=500
            )

# get list of negotiations for a customer
@customer_negotiation_ns.route('/negotiations/<int:customer_id>')
class CustomerNegotiationList(Resource):
    @customer_negotiation_ns.marshal_list_with(negotiation_model)
    def get(self, customer_id):
        '''List all negotiations for a customer'''
        try:
            negotiations = NegotiationService.get_negotiations_for_customer(customer_id)
            if not negotiations:
                return standardize_response(
                    status='fail',
                    message='No negotiations found for customer',
                    code=404
                )
            return standardize_response(
                status='success',
                data=negotiations,
                code=200
            )
        except Exception as e:
            current_app.logger.error(e)
            return standardize_response(
                status='fail',
                message='Failed to get negotiations for customer',
                code=500
            )
        
# negotiation details, additional offer
@customer_negotiation_ns.route('/negotiation/<int:negotiation_id>')
class CustomerNegotiationDetails(Resource):
    # get negotiation details
    @customer_negotiation_ns.marshal_with(negotiation_details_model)
    def get(self, negotiation_id):
        '''Get negotiation details'''
        try:
            negotiation, offers = NegotiationService.get_negotiation_details(negotiation_id)
            if not negotiation:
                return standardize_response(
                    status='fail',
                    message='Negotiation not found',
                    code=404
                )
            return standardize_response(
                status='success',
                data={
                    'negotiation': negotiation,
                    'offers': offers
                },
                code=200
            )
        except Exception as e:
            current_app.logger.error(e)
            return standardize_response(
                status='fail',
                message='Failed to get negotiation details',
                code=500
            )

    # place additional offer
    @customer_negotiation_ns.marshal_with(offer_model)
    def post(self, negotiation_id):
        '''Place additional offer'''
        try:
            data = customer_negotiation_ns.payload
            offer_price = data['offer_price']
            offer_id = NegotiationService.additional_offer(negotiation_id, offer_price)
            return standardize_response(
                status='success',
                data={'offer_id': offer_id},
                code=201
            )
        except Exception as e:
            current_app.logger.error(e)
            return standardize_response(
                status='fail',
                message='Failed to place additional offer',
                code=500
            )
        
# accept offer
@customer_negotiation_ns.route('/negotiation/<int:negotiation_id>/accept')
class CustomerNegotiationAccept(Resource):
    def post(self, negotiation_id):
        '''Accept offer'''
        try:
            NegotiationService.accept_offer(negotiation_id)
            return standardize_response(
                status='success',
                message='Offer accepted',
                code=200
            )
        except Exception as e:
            current_app.logger.error(e)
            return standardize_response(
                status='fail',
                message='Failed to accept offer',
                code=500
            )

# regect counter offer
@customer_negotiation_ns.route('/negotiation/<int:negotiation_id>/reject')
class CustomerNegotiationReject(Resource):
    def post(self, negotiation_id):
        '''Reject offer'''
        try:
            NegotiationService.reject_offer(negotiation_id)
            return standardize_response(
                status='success',
                message='Offer rejected',
                code=200
            )
        except Exception as e:
            current_app.logger.error(e)
            return standardize_response(
                status='fail',
                message='Failed to reject offer',
                code=500
            )
    
    
        
