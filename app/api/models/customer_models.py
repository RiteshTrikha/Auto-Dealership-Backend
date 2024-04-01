from flask_restx import fields, Model

customer_model = Model('Customer', {
    'customer_id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'ssn': fields.String,
    'birth_date': fields.Date,
    'drivers_license': fields.String,
    'address_id': fields.Integer,
    'create_time': fields.DateTime,
    'status': fields.Integer
})

credit_report_model = Model('CreditReport', {
    'credit_report_id': fields.Integer,
    'customer_id': fields.Integer,
    'score': fields.Integer
})

customer_vehical_model = Model('CustomerVehical', {
    'customer_vehical_id': fields.Integer,
    'vin': fields.String,
    'year': fields.String,
    'make': fields.String,
    'model': fields.String,
    'customer_id': fields.Integer
})