from flask import Blueprint
from flask_restx import Api

from .namespaces.customer_negotiation_ns import customer_negotiation_ns
from .namespaces.user_negotiation_ns import user_negotiation_ns
from .namespaces.inventory_ns import inventory_ns

api_bp = Blueprint('api', __name__)
api = Api(
    title='Dealership API',
    version='1.0',
    description='A simple API for a dealership',
)

api.add_namespace(customer_negotiation_ns , path='/customer/negotiation')
api.add_namespace(user_negotiation_ns , path='/user/negotiation')
api.add_namespace(inventory_ns , path='/inventory')