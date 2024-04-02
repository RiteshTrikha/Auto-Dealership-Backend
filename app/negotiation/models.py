from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from enum import IntEnum

class Negotiation(db.Model):
    __tablename__ = 'negotiation'

    class NegotiationStatus(IntEnum):
        ACTIVE = 1
        ACCEPTED = 2
        REJECTED = 3

    negotiation_id = Column(INTEGER, primary_key=True, unique=True)
    vehical_id = Column(ForeignKey('vehical.vehical_id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    negotiation_status = Column(Integer, nullable=False, server_default=text("1"))
    start_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    end_date = Column(DateTime)

    customer = relationship('app.customer.models.Customer' , backref='negotiations')
    vehical = relationship('app.inventory.models.Vehical' , backref='negotiations')

    # functions
    def serialize(self):
        return {
            'negotiation_id': self.negotiation_id,
            'vehical_id': self.vehical_id,
            'customer_id': self.customer_id,
            'negotiation_status': self.negotiation_status,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
    
    # create functions
    @classmethod
    def create_negotiation(cls, vehical_id, customer_id):
        try:
            # create negotiation
            negotiation = Negotiation(vehical_id=vehical_id, customer_id=customer_id)
            db.session.add(negotiation)
            db.session.commit()
            return negotiation
        except Exception as e:
            raise e
        
    # update functions
    @classmethod
    def update_negotiation_status(cls, negotiation_id, negotiation_status):
        try:
            # update negotiation status
            negotiation = db.session.query(Negotiation).filter(Negotiation.negotiation_id == negotiation_id).first()
            negotiation.negotiation_status = negotiation_status
            db.session.commit()
        except Exception as e:
            raise e


    # get functions
    @classmethod
    def get_negotiation(cls, negotiation_id):
        try:
            # get negotiation
            negotiation = db.session.query(Negotiation).filter(Negotiation.negotiation_id == negotiation_id).first()
            return negotiation
        except Exception as e:
            raise e

    @classmethod
    def get_negotiations(cls, customer_id):
        try:
            # get all negotiations for a customer
            negotiations = db.session.query(Negotiation).filter(Negotiation.customer_id == customer_id).all()
            return negotiations
        except Exception as e:
            raise e
        
    @classmethod
    def get_all_negotiations(cls):
        try:
            # get all negotiations
            negotiations = db.session.query(Negotiation).all()
            return negotiations
        except Exception as e:
            raise e
        
    @classmethod
    def negotiation_already_exists(cls, vehical_id, customer_id):
        try:
            # check if negotiation already exists
            negotiation = db.session.query(Negotiation).filter(Negotiation.vehical_id == vehical_id, Negotiation.customer_id == customer_id).first()
            if negotiation:
                return True
            return False
        except Exception as e:
            raise e
    

class Offer(db.Model):
    __tablename__ = 'offer'

    class OfferType(IntEnum):
        OFFER = 1
        COUNTER_OFFER = 2

    class OfferStatus(IntEnum):
        PENDING = 1
        ACCEPTED = 2
        REJECTED = 3
        COUNTERED = 4

    offer_id = Column(INTEGER, primary_key=True, unique=True)
    negotiation_id = Column(ForeignKey('negotiation.negotiation_id'), nullable=False, index=True)
    offer_type = Column(Integer, nullable=False)
    offer_price = Column(Integer, nullable=False)
    offer_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    offer_status = Column(Integer, nullable=False, server_default=text("1"))
    message = Column(String(512))

    negotiation = relationship('Negotiation')

    # functions
    def serialize(self):
        return {
            'offer_id': self.offer_id,
            'negotiation_id': self.negotiation_id,
            'offer_type': self.offer_type,
            'offer_price': self.offer_price,
            'offer_date': self.offer_date,
            'offer_status': self.offer_status,
            'message': self.message
        }
    
    # create functions
    @classmethod
    def create_offer(cls, negotiation_id, offer_type, offer_price, message=None):
        try:
            # create offer
            offer = Offer(negotiation_id=negotiation_id, offer_type=offer_type, offer_price=offer_price, message=message, offer_status=1)
            db.session.add(offer)
            db.session.commit()
            return offer
        except Exception as e:
            raise e
        
    # get functions
    @classmethod
    def get_offers(cls, negotiation_id):
        try:
            # get all offers for a negotiation
            offers = db.session.query(Offer).filter(Offer.negotiation_id == negotiation_id).all()
            return offers
        except Exception as e:
            raise e
        
    @classmethod
    def update_current_offer_status(cls, negotiation_id, offer_status):
        try:
            # update current offer status
            offer = db.session.query(Offer).filter(Offer.negotiation_id == negotiation_id).order_by(Offer.offer_id.desc()).first()
            offer.offer_status = offer_status
            db.session.commit()
        except Exception as e:
            raise e
        
    @classmethod
    def update_previous_offer_status(cls, negotiation_id, offer_status):
        try:
            # update previous offer status
            offer = db.session.query(Offer).filter(Offer.negotiation_id == negotiation_id).order_by(Offer.offer_id.desc()).offset(1).first()
            offer.offer_status = offer_status
            db.session.commit()
        except Exception as e:
            raise e
        
    @classmethod
    def current_offer_is_counter_offer(cls, negotiation_id):
        try:
            # get current offer
            offer = db.session.query(Offer).filter(Offer.negotiation_id == negotiation_id).order_by(Offer.offer_id.desc()).first()
            if offer.offer_type == Offer.OfferType.COUNTER_OFFER:
                return True
            return False
        except Exception as e:
            raise e
        
    @classmethod
    def current_offer_is_offer(cls, negotiation_id):
        try:
            # get current offer
            offer = db.session.query(Offer).filter(Offer.negotiation_id == negotiation_id).order_by(Offer.offer_id.desc()).first()
            if offer.offer_type == Offer.OfferType.OFFER:
                return True
            return False
        except Exception as e:
            raise e