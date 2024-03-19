from flask import jsonify, request
from . import shared_bp
from .models import *
from app import db

@shared_bp.route('/api/shared/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from shared_bp!'})

@shared_bp.route('/api/shared/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.query(Customer).filter(Customer.customer_id == customer_id).first()
    if customer:
        return jsonify(customer.serialize())
    else:
        return jsonify({'message': 'Customer not found'}), 404

