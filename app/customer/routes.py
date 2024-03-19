from flask import jsonify, request
from . import customer_bp
from .models import *
from app import db

@customer_bp.route('/api/customer/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from customer_bp!'})

@customer_bp.route('/api/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.query(Customer).filter(Customer.customer_id == customer_id).first()
    if customer:
        return jsonify(customer.serialize())
    else:
        return jsonify({'message': 'Customer not found'}), 404

