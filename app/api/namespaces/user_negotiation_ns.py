from flask_restx import Namespace, Resource, fields
from ..models.negotiation_models import negotiation_model, negotiation_details_model, offer_model
# import services
from app.negotiation.services import NegotiationService
# import utilities
from app.api.utilities import Utilities
standardize_response = Utilities().standardize_response

user_negotiation_ns = Namespace('UserNegotiation', description='User Negotiation related operations')

# register models with namespace
user_negotiation_ns.models[negotiation_model.name] = negotiation_model
user_negotiation_ns.models[offer_model.name] = offer_model
user_negotiation_ns.models[negotiation_details_model.name] = negotiation_details_model

# routes

# get list of all negotiations
@user_negotiation_ns.route('/negotiations')
class UserNegotiationList(Resource):
    @user_negotiation_ns.marshal_list_with(negotiation_model)
    def get(self):
        '''List all negotiations'''
        try:
            negotiations = NegotiationService().get_all_negotiations()
            if not negotiations:
                return standardize_response(
                    status='fail',
                    message='No negotiations found',
                    code=404
                )
            return standardize_response(
                status='success',
                data=negotiations,
                code=200
            )
        except Exception as e:
            return standardize_response(
                status='fail',
                message='Failed to get negotiations',
                code=500
            )
        
# get negotiation details, counter offer
@user_negotiation_ns.route('/negotiations/<int:negotiation_id>')
class UserNegotiation(Resource):
    # get negotiation details
    @user_negotiation_ns.marshal_with(negotiation_details_model)
    def get(self, negotiation_id):
        '''Get negotiation details'''
        try:
            negotiation, offers = NegotiationService().get_negotiation_details(negotiation_id)
            if not negotiation:
                return standardize_response(
                    status='fail',
                    message='Negotiation not found',
                    code=404
                )
            return standardize_response(
                status='success',
                data={'negotiation': negotiation.serialize(), 'offers': [offer.serialize() for offer in offers]},
                code=200
            )
        except Exception as e:
            return standardize_response(
                status='fail',
                message='Failed to get negotiation details',
                code=500
            )
        
    # counter offer
    @user_negotiation_ns.expect(offer_model)
    def post(self, negotiation_id):
        '''Counter offer'''
        try:
            data = user_negotiation_ns.payload
            offer_price = data['offer_price']
            offer_id = NegotiationService().counter_offer(negotiation_id, offer_price)
            return standardize_response(
                status='success',
                message='Counter offer created',
                data={'offer_id': offer_id},
                code=201
            )
        except Exception as e:
            return standardize_response(
                status='fail',
                message='Failed to create counter offer',
                code=500
            )
        
# accept offer
@user_negotiation_ns.route('/negotiations/<int:negotiation_id>/accept')
class UserNegotiationAccept(Resource):
    def post(self, negotiation_id):
        '''Accept offer'''
        try:
            NegotiationService().accept_offer(negotiation_id)
            return standardize_response(
                status='success',
                message='Offer accepted',
                code=200
            )
        except Exception as e:
            return standardize_response(
                status='fail',
                message='Failed to accept offer',
                code=500
            )

# reject offer
@user_negotiation_ns.route('/negotiations/<int:negotiation_id>/reject')
class UserNegotiationReject(Resource):
    def post(self, negotiation_id):
        '''Reject offer'''
        try:
            NegotiationService().reject_offer(negotiation_id)
            return standardize_response(
                status='success',
                message='Offer rejected',
                code=200
            )
        except Exception as e:
            return standardize_response(
                status='fail',
                message='Failed to reject offer',
                code=500
            )

