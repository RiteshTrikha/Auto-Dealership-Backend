from app import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, INTEGER, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()
metadata = Base.metadata

class Negotiation(Base):
    __tablename__ = 'negotiation'

    negotiation_id = Column(INTEGER, primary_key=True, unique=True)
    vehical_id = Column(ForeignKey('vehical.vehical_id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.customer_id'), nullable=False, index=True)
    negotiation_status = Column(INTEGER, nullable=False)
    start_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    end_date = Column(DateTime)

    customer = relationship('Customer')
    vehical = relationship('Vehical')

    # functions
    def serialize(self):
        return {
            'negotiation_id': self.negotiation_id,
            'vehical_id': self.vehical_id,
            'customer_id': self.customer_id,
            'negotiation_status': self.negotiation_status,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
    
    # place offer / create negotiation
    def create_negotiation(self, vehical_id, customer_id, offer_price):
        # create negotiation
        negotiation = Negotiation(vehical_id=vehical_id, customer_id=customer_id, negotiation_status=1)
        db.session.add(negotiation)
        db.session.commit()
        # create offer
        offer = Offer(negotiation_id=negotiation.negotiation_id, offer_price=offer_price, offer_status=1)
        db.session.add(offer)
        db.session.commit()
        return negotiation.negotiation_id
    
    # get all negotiations for a customer
    def get_negotiations(self, customer_id):
        negotiations = db.session.query(Negotiation).filter(Negotiation.customer_id == customer_id).all()
        return negotiations
    
    # get all negotiations for management
    def get_all_negotiations(self):
        negotiations = db.session.query(Negotiation).all()
        return negotiations
    
    # get negotiation by id
    def get_negotiation_plus_offers(self, negotiation_id):
        # get negotiation by id and all related offers and counter offers
        negotiation = db.session.query(Negotiation).filter(Negotiation.negotiation_id == negotiation_id).first()
        if negotiation:
            # get all offers for negotiation
            offers = db.session.query(Offer).filer(Offer.negotiation_id == negotiation_id).all()
            # get all counter offers for negotiation
            counter_offers = db.session.query(CounterOffer).filter(CounterOffer.offer_id.in_([offer.offer_id for offer in offers])).all()

        return negotiation, offers, counter_offers
    
    # create counter offer
    def create_counter_offer(self, offer_id, counter_price):
        # create counter offer
        counter_offer = CounterOffer(offer_id=offer_id, counter_price=counter_price, counter_status=1)
        # update offer status
        offer = db.session.query(Offer).filter(Offer.offer_id == offer_id).first()
        offer.offer_status = 4
        return counter_offer.counter_offer_id
    
    # create additional offer in response to counter offer
    def create_additional_offer(self, negotiation_id, offer_price):
        # create offer
        offer = Offer(negotiation_id=negotiation_id, offer_price=offer_price, offer_status=1)
        db.session.add(offer)
        db.session.commit()
        # set counter offer status to 4
        counter_offer = db.session.query(CounterOffer).filter(CounterOffer.offer_id == offer.offer_id - 1).first()
        if counter_offer:
            counter_offer.counter_status = 4
        return offer.offer_id
    
    # accept offer
    def accept_offer(self, offer_id):
        # update offer status
        offer = db.session.query(Offer).filter(Offer.offer_id == offer_id).first()
        offer.offer_status = 2
        # update negotiation status
        negotiation = db.session.query(Negotiation).filter(Negotiation.negotiation_id == offer.negotiation_id).first()
        negotiation.negotiation_status = 2
        return offer.offer_id


class Offer(Base):
    __tablename__ = 'offer'

    #enum('pending', 'accepted', 'rejected')
    class OfferStatus(Enum):
        PENDING = 1
        ACCEPTED = 2
        REJECTED = 3
        COUNTERED = 4

    offer_id = Column(INTEGER, primary_key=True, unique=True)
    negotiation_id = Column(ForeignKey('negotiation.negotiation_id'), nullable=False, index=True)
    offer_price = Column(INTEGER, nullable=False)
    offer_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    offer_status = Column(INTEGER, nullable=False)

    negotiation = relationship('Negotiation')

    # functions
    def serialize(self):
        return {
            'offer_id': self.offer_id,
            'negotiation_id': self.negotiation_id,
            'offer_price': self.offer_price,
            'offer_date': self.offer_date,
            'offer_status': self.offer_status
        }


class CounterOffer(Base):
    __tablename__ = 'counter_offer'

    class CounterStatus(Enum):
        PENDING = 1
        ACCEPTED = 2
        REJECTED = 3
        COUNTERED = 4

    counter_offer_id = Column(INTEGER, primary_key=True, unique=True)
    offer_id = Column(ForeignKey('offer.offer_id'), nullable=False, unique=True)
    counter_price = Column(INTEGER, nullable=False)
    counter_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    counter_status = Column(INTEGER, nullable=False)

    offer = relationship('Offer')

    # functions
    def serialize(self):
        return {
            'counter_offer_id': self.counter_offer_id,
            'offer_id': self.offer_id,
            'counter_price': self.counter_price,
            'counter_date': self.counter_date,
            'counter_status': self.counter_status
        }