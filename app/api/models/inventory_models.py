from flask_restx import fields, Model

vehical_model = Model('Vehical', {
    'vehical_id': fields.Integer,
    'vin': fields.String,
    'price': fields.Float,
    'year': fields.String,
    'make': fields.String,
    'model': fields.String,
    'miles': fields.Integer,
    'mpg': fields.Integer,
    'color': fields.String,
    'fuel_type': fields.String,
    'transmission': fields.String,
    'image': fields.String,
    'vehical_status': fields.Integer
})

retail_item_model = Model('RetailItem', {
    'retail_item_id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'description': fields.String,
    'image': fields.String,
    'item_status': fields.Integer
})