from flask_restx import fields, Model

negotiation_model = Model('Negotiation', {
    'negotiation_id': fields.Integer,
    'vehical_id': fields.Integer,
    'customer_id': fields.Integer,
    'negotiation_status': fields.Integer,
    'start_date': fields.DateTime,
    'end_date': fields.DateTime
})

offer_model = Model('Offer', {
    'offer_id': fields.Integer,
    'negotiation_id': fields.Integer,
    'offer_price': fields.Float,
    'offer_status': fields.Integer,
    'offer_date': fields.DateTime
})

negotiation_details_model = Model('NegotiationDetails', {
    'negotiation': fields.Nested(negotiation_model),
    'offers': fields.List(fields.Nested(offer_model))
})

create_negotiation_model = Model('CreateNegotiation', {
    'vehicle_id': fields.Integer,
    'customer_id': fields.Integer,
    'offer_price': fields.Float
})