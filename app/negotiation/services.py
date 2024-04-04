from flask import current_app, g
from .models import Negotiation, Offer
from app.exceptions import ExposedException, ExpDatabaseException
from app import db

class NegotiationService:
    # logic for negotiations
    
    # place offer / create negotiation
    def create_negotiation(self, vehical_id, customer_id, offer_price, message):
        try:
            # check if negotiation already exists for vehical and customer
            if Negotiation.negotiation_already_exists(vehical_id, customer_id):
                raise ExposedException('Negotiation already in progress for vehical and customer', code=400)
            # create negotiation
            negotiation = Negotiation.create_negotiation(vehical_id, customer_id)
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation.negotiation_id, offer_type=Offer.OfferType.OFFER.value, 
                                       offer_price=offer_price, message=message)
            db.session.commit()
            return {'negotiation_id': negotiation.negotiation_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
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
                    'vehical': {
                        'vehical_id': negotiation.vehical_id,
                        'year': negotiation.vehical.year,
                        'make': negotiation.vehical.make,
                        'model': negotiation.vehical.model,
                        'image': negotiation.vehical.image
                    },
                    'customer_id': negotiation.customer_id,
                    'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
                    'start_date': negotiation.start_date,
                    'end_date': negotiation.end_date

                } for negotiation in negotiations]
            }
        except Exception as e:
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
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
                    'vehical_id': negotiation.vehical_id,
                    'customer_id': negotiation.customer_id,
                    'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
                    'start_date': negotiation.start_date,
                    'end_date': negotiation.end_date
                } for negotiation in negotiations]
            }
        except Exception as e:
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
    # get negotiation details
    def get_negotiation_details(self, negotiation_id):
        try:
            # get negotiation
            negotiation = Negotiation.get_negotiation(negotiation_id)
            offers = Offer.get_offers(negotiation_id)
            if negotiation is None:
                raise ExposedException('Negotiation not found', code=404)
            return {
                'negotiation': {
                    'negotiation_id': negotiation.negotiation_id,
                    'customer_id': negotiation.customer_id,
                    'negotiation_status': Negotiation.NegotiationStatus(negotiation.negotiation_status).name,
                    'start_date': negotiation.start_date,
                    'end_date': negotiation.end_date
                },
                'offers': [{
                        'offer_id': offer.offer_id,
                        'offer_type': Offer.OfferType(offer.offer_type).name,
                        'offer_price': offer.offer_price,
                        'offer_date': offer.offer_date,
                        'offer_status': Offer.OfferStatus(offer.offer_status).name,
                        'message': offer.message
                    } for offer in offers],
                'vehicle': {
                    'vehical_id': negotiation.vehical_id,
                    'year': negotiation.vehical.year,
                    'make': negotiation.vehical.make,
                    'model': negotiation.vehical.model,
                    'image': negotiation.vehical.image
                }
            }
        except Exception as e:
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
    # counter offer
    def counter_offer(self, negotiation_id, offer_price, message=None):
        try:
            if Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for additional offer before placing another counter offer')
            # update current offer status
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.COUNTERED.value)
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation_id, offer_type=Offer.OfferType.COUNTER_OFFER.value,
                                       offer_price=offer_price, message=message)
            db.session.commit()
            return {'offer_id': offer.offer_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
    # additional offer
    def additional_offer(self, negotiation_id, offer_price, message=None):
        try:
            # check if most recent offer is a counter offer
            if not Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for counter offer before placing additional offer')
            # update current offer status
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.COUNTERED.value)
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation_id, offer_type=Offer.OfferType.OFFER.value, 
                                       offer_price=offer_price, message=message)
            db.session.commit()
            return {'offer_id': offer.offer_id}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
    # accept offer
    def accept_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for a response to counter offer')
            # update negotiation status to 2 (accepted)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.ACCEPTED.value)
            # update offer status to 2 (accepted)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.ACCEPTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
    def accept_counter_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for a response to offer')
            # update negotiation status to 2 (accepted)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.ACCEPTED.value)
            # update offer status to 2 (accepted)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.ACCEPTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise ExpDatabaseException
        
    # reject offer
    def reject_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for a response to counter offer')
            # update negotiation status to 3 (rejected)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.REJECTED.value)
            # update offer status to 3 (rejected)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.REJECTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise ExpDatabaseException
    
    # reject counter offer
    def reject_counter_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for a response to offer')
            # update negotiation status to 3 (rejected)
            Negotiation.update_negotiation_status(negotiation_id, Negotiation.NegotiationStatus.REJECTED.value)
            # update offer status to 3 (rejected)
            Offer.update_current_offer_status(negotiation_id, Offer.OfferStatus.REJECTED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            raise ExpDatabaseException