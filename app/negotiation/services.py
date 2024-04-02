from flask import current_app, g
from .models import Negotiation, Offer
from app.exceptions import ExposedException

class NegotiationService:
    # logic for negotiations
    
    # place offer / create negotiation
    def create_negotiation(self, vehical_id, customer_id, offer_price, message):
        try:
            # check if negotiation already exists for vehical and customer
            if Negotiation.negotiation_already_exists(vehical_id, customer_id):
                raise ExposedException('Negotiation already in progress for vehical and customer')
            # create negotiation
            negotiation = Negotiation.create_negotiation(vehical_id, customer_id)
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation.negotiation_id, offer_type=int(Offer.OfferType.OFFER), 
                                       offer_price=offer_price, message=message)
            return negotiation.negotiation_id
        except Exception as e:
            raise e
        
    # get negotiations for a customer
    def get_negotiations(self, customer_id):
        try:
            # get all negotiations for a customer
            negotiations = Negotiation.get_negotiations(customer_id)
            return negotiations
        except Exception as e:
            raise e
        
    # get all negotiations
    def get_all_negotiations(self):
        try:
            # get all negotiations
            negotiations = Negotiation.get_all_negotiations()
            return negotiations
        except Exception as e:
            raise e
        
    # get negotiation details
    def get_negotiation_details(self, negotiation_id):
        try:
            # get negotiation
            negotiation = Negotiation.get_negotiation(negotiation_id)
            offers = Offer.get_offers(negotiation_id)
            return negotiation, offers
        except Exception as e:
            raise e
        
    # counter offer
    def counter_offer(self, negotiation_id, offer_price, message=None):
        try:
            if Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for additional offer before placing another counter offer')
            # update current offer status
            Offer.update_current_offer_status(negotiation_id, int(Offer.OfferStatus.COUNTERED))
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation_id, offer_type=int(Offer.OfferType.COUNTER_OFFER), 
                                       offer_price=offer_price, message=message)
            return offer.offer_id
        except Exception as e:
            raise e
        
    # additional offer
    def additional_offer(self, negotiation_id, offer_price, message=None):
        try:
            # check if most recent offer is a counter offer
            if not Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for counter offer before placing additional offer')
            # update current offer status
            Offer.update_current_offer_status(negotiation_id, int(Offer.OfferStatus.COUNTERED))
            # create offer
            offer = Offer.create_offer(negotiation_id=negotiation_id, offer_type=int(Offer.OfferType.OFFER), 
                                       offer_price=offer_price, message=message)
            return offer.offer_id
        except Exception as e:
            raise e
        
    # accept offer
    def accept_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for a response to counter offer')
            # update negotiation status to 2 (accepted)
            Negotiation.update_negotiation_status(negotiation_id, int(Negotiation.NegotiationStatus.ACCEPTED))
            # update offer status to 2 (accepted)
            Offer.update_current_offer_status(negotiation_id, int(Offer.OfferStatus.ACCEPTED))
        except Exception as e:
            raise e
        
    def accept_counter_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for a response to offer')
            # update negotiation status to 2 (accepted)
            Negotiation.update_negotiation_status(negotiation_id, int(Negotiation.NegotiationStatus.ACCEPTED))
            # update offer status to 2 (accepted)
            Offer.update_current_offer_status(negotiation_id, int(Offer.OfferStatus.ACCEPTED))
        except Exception as e:
            raise e
        
    # reject offer
    def reject_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_counter_offer(negotiation_id):
                raise ExposedException('Must wait for a response to counter offer')
            # update negotiation status to 3 (rejected)
            Negotiation.update_negotiation_status(negotiation_id, int(Negotiation.NegotiationStatus.REJECTED))
            # update offer status to 3 (rejected)
            Offer.update_current_offer_status(negotiation_id, int(Offer.OfferStatus.REJECTED))
        except Exception as e:
            raise e
        
    def reject_counter_offer(self, negotiation_id):
        try:
            if Offer.current_offer_is_offer(negotiation_id):
                raise ExposedException('Must wait for a response to offer')
            # update negotiation status to 3 (rejected)
            Negotiation.update_negotiation_status(negotiation_id, int(Negotiation.NegotiationStatus.REJECTED))
            # update offer status to 3 (rejected)
            Offer.update_current_offer_status(negotiation_id, int(Offer.OfferStatus.REJECTED))
        except Exception as e:
            raise e