from flask import current_app, g
from .models import Negotiation, Offer
from app.exceptions import ExposedException, ExpDatabaseException
from app import db

class NegotiationService:
    # logic for negotiations
    
    # place offer / create negotiation
    def create_negotiation(self, vehicle_id, customer_id, offer_price, message):
        try:
                  #check for missing fields
            if not customer_id or not vehicle_id or not offer_price:
                raise ExposedException('Missing required fields', code=400)
            # check if negotiation already exists for vehicle and customer
            if Negotiation.negotiation_already_exists(vehicle_id, customer_id):
                raise ExposedException('Negotiation already in progress for vehicle and customer', code=400)
            # create negotiation
            negotiation = Negotiation.create_negotiation(vehicle_id, customer_id)
            db.session.commit()
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation.negotiation_id, offer_type=Offer.OfferType.OFFER.value, 
                                       offer_price=offer_price, message=message)
            db.session.commit()
            return {'negotiation_id': negotiation.negotiation_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    # get negotiations for a customer
    def get_negotiations(self, customer_id):
        try:
            # get all negotiations for a customer
            negotiations = Negotiation.get_negotiations(customer_id)
            if negotiations == []:
                raise ExposedException('No negotiations found for customer')
            return {
                'negotiations': [{
                    'negotiation_id': negotiation.negotiation_id,
                    'vehicle': {
                        'vehicle_id': negotiation.vehicle_id,
                        'year': negotiation.vehicle.year,
                        'make': negotiation.vehicle.make,
                        'model': negotiation.vehicle.model,
                        'image': negotiation.vehicle.image
                    },
                    'customer_id': negotiation.customer_id,
                    'current_offer': negotiation.offers[-1].offer_price,
                    'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
                    'start_date': negotiation.start_date,
                    'end_date': negotiation.end_date

                } for negotiation in negotiations]
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    # get all negotiations
    def get_all_negotiations(self):
        try:
            # get all negotiations
            negotiations = Negotiation.get_all_negotiations()
            if negotiations == []:
                raise ExposedException('No negotiations found', code=404)
            return {
                'negotiations': [{
                    'negotiation_id': negotiation.negotiation_id,
                    'vehicle': {
                        'vehicle_id': negotiation.vehicle_id,
                        'year': negotiation.vehicle.year,
                        'make': negotiation.vehicle.make,
                        'model': negotiation.vehicle.model,
                        'image': negotiation.vehicle.image
                    },
                    'customer_id': negotiation.customer_id,
                    'current_offer': negotiation.offers[-1].offer_price,
                    'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
                    'start_date': negotiation.start_date,
                    'end_date': negotiation.end_date
                } for negotiation in negotiations]
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    # get accepted negotiation by customer
    def get_accepted_negotiation(self, customer_id, negotiation_id):
        try:
            # get negotiation
            negotiation = Negotiation.get_negotiation(negotiation_id)
            if negotiation is None:
                raise ExposedException('Negotiation not found', code=404)
            if negotiation.negotiation_status != Negotiation.NegotiationStatus.ACCEPTED.value:
                raise ExposedException('Negotiation not accepted', code=400)
            if negotiation.customer_id != customer_id:
                current_app.logger.info(f'Customer {customer_id} attempted to access negotiation {negotiation_id} belonging to customer {negotiation.customer_id}')
                raise ExposedException('Negotiation not found for customer', code=404)
            return negotiation
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    # get negotiation
    def get_negotiation(self, negotiation_id):
        try:
            # get negotiation
            negotiation = Negotiation.get_negotiation(negotiation_id)
            if negotiation is None:
                raise ExposedException('Negotiation not found', code=404)
            return {
                'negotiation_id': negotiation.negotiation_id,
                'customer': {
                    'customer_id': negotiation.customer_id,
                    'first_name': negotiation.customer.first_name,
                    'last_name': negotiation.customer.last_name,
                },
                'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
                'start_date': negotiation.start_date,
                'end_date': negotiation.end_date,
                'current_offer': negotiation.offers[-1].offer_price,
                'vehicle': {
                    'vehicle_id': negotiation.vehicle_id,
                    'year': negotiation.vehicle.year,
                    'make': negotiation.vehicle.make,
                    'model': negotiation.vehicle.model,
                    'image': negotiation.vehicle.image
                }
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    # get negotiation details
    def get_negotiation_details(self, negotiation_id):
        try:
            # get negotiation
            negotiation = Negotiation.get_negotiation(negotiation_id)
            offers = Offer.get_offers(negotiation_id)
            if negotiation is None:
                raise ExposedException('Negotiation not found', code=404)
            return {
                'negotiation_id': negotiation.negotiation_id,
                'customer': {
                    'customer_id': negotiation.customer_id,
                    'first_name': negotiation.customer.first_name,
                    'last_name': negotiation.customer.last_name,
                },
                'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
                'start_date': negotiation.start_date,
                'end_date': negotiation.end_date,
                'current_offer': negotiation.offers[-1].offer_price,
                'offers': [{
                        'offer_id': offer.offer_id,
                        'offer_type': Offer.OfferType(offer.offer_type).name,
                        'offer_price': offer.offer_price,
                        'offer_date': offer.offer_date,
                        'offer_status': Offer.OfferStatus(offer.offer_status).name,
                        'message': offer.message
                    } for offer in offers],
                'vehicle': {
                    'vehicle_id': negotiation.vehicle_id,
                    'year': negotiation.vehicle.year,
                    'make': negotiation.vehicle.make,
                    'model': negotiation.vehicle.model,
                    'image': negotiation.vehicle.image
                }
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
    # counter offer
    def counter_offer(self, negotiation_id, offer_price, message=None):
        try:
            if Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for a response to your counter offer')
            # update current offer status
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.COUNTERED.value)
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation_id, offer_type=Offer.OfferType.COUNTER_OFFER.value,
                                       offer_price=offer_price, message=message)
            db.session.commit()
            return {'offer_id': offer.offer_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    # additional offer
    def additional_offer(self, negotiation_id, offer_price, message=None):
        try:
            current_app.logger.info(f'negotiation_id: {negotiation_id}')
            # check if most recent offer is a counter offer
            if Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for a response to your counter offer')
            # update current offer status
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.COUNTERED.value)
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation_id, offer_type=Offer.OfferType.OFFER.value, 
                                       offer_price=offer_price, message=message)
            current_app.logger.info(f'offer_id: {offer.offer_id}')
            db.session.commit()
            return {'offer_id': offer.offer_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    # accept offer
    def accept_offer(self, negotiation_id):
        try:
            if not Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for a response to your counter offer')
            # update negotiation status to 2 (accepted)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.ACCEPTED.value)
            # update offer status to 2 (accepted)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.ACCEPTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    def accept_counter_offer(self, negotiation_id):
        try:
            if not Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for a response to your offer')
            # update negotiation status to 2 (accepted)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.ACCEPTED.value)
            # update offer status to 2 (accepted)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.ACCEPTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
    # reject offer
    def reject_offer(self, negotiation_id):
        try:
            if not Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for a response to offer')
            # update negotiation status to 3 (rejected)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.REJECTED.value)
            # update offer status to 3 (rejected)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.REJECTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
    
    # reject counter offer
    def reject_counter_offer(self, negotiation_id):
        try:
            if not Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for a response to offer')
            # update negotiation status to 3 (rejected)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.REJECTED.value)
            # update offer status to 3 (rejected)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.REJECTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e

