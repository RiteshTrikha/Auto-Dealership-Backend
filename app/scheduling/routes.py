from flask import jsonify, request
from . import scheduling_bp
from .models import *
from app import db

@scheduling_bp.route('/api/scheduling/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from scheduling_bp!'})

@scheduling_bp.route('/api/scheduling/time-slot-available', methods=['GET'])
def get_time_slots():
    try:
        time_slots = TimeSlot.get_available_time_slots()
        if time_slots is None:
            return jsonify(
                status='fail',
                data=[],
                message='No time slots available'
                ), 404
        return jsonify(
            status='success',
            data=[time_slot.serialize() for time_slot in time_slots],
            message='Time slots retrieved successfully'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail',
            data=[],
            message=str(e)
            ), 400
    
@scheduling_bp.route('/api/scheduling/time-slots', methods=['GET'])
def get_all_time_slots():
    try:
        time_slots = TimeSlot.get_all_time_slots()
        if time_slots is None:
            return jsonify(
                status='fail',
                data=[],
                message='No time slots available'
                ), 404
        return jsonify(
            status='success',
            data=[time_slot.serialize() for time_slot in time_slots],
            message='Time slots retrieved successfully'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail',
            data=[],
            message=str(e)
            ), 400
    
@scheduling_bp.route('/api/scheduling/appointments', methods=['GET'])
def get_appointments():
    try:
        appointments = Appointment.get_all_appointments()
        if appointments is None:
            return jsonify(
                status='fail',
                data=[],
                message='No appointments available'
                ), 404
        return jsonify(
            status='success',
            data=[appointment.serialize() for appointment in appointments],
            message='Appointments retrieved successfully'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail',
            data=[],
            message=str(e)
            ), 400
    
@scheduling_bp.route('/api/scheduling/appointment/<appointment_id>', methods=['GET'])
def get_appointment():
    try:
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if appointment is None:
            return jsonify(
                status='fail',
                data=[],
                message='Appointment not found'
                ), 404
        return jsonify(
            status='success',
            data= appointment.serialize(),
            message='Appointment retrieved successfully'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail',
            data=[],
            message=str(e)
            ), 400

@scheduling_bp.route('/api/scheduling/create_appointment', methods=['POST'])
def create_appointment():
    try:
        


@scheduling_bp.route('/api/scheduling/appointment_details', methods=['POST'])
def get_appointment_details():
    try:
        data = request.get_json()
        appointment_id = data['appointment_id']
        appointment_details = AppointmentDetail.get_all_appointment_details(appointment_id)
        if appointment_details is None:
            return jsonify(
                status='fail',
                data=[],
                message='No appointment details available'
                ), 404
        return jsonify(
            status='success',
            data=[appointment_detail.serialize() for appointment_detail in appointment_details],
            message='Appointment details retrieved successfully'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail',
            data=[],
            message=str(e)
            ), 400
    
@scheduling_bp.route('/api/scheduling/appointment_details/<appointment_details_id>', methods=['GET'])
def get_appointment_detail():
    try:
        appointment_details = AppointmentDetail.get_appointment_details_by_appointment_details_id(appointment_details_id)
        if appointment_details is None:
            return jsonify(
                status='fail',
                data=[],
                message='Appointment details not found'
                ), 404
        return jsonify(
            status='success',
            data= appointment_details.serialize(),
            message='Appointment details retrieved successfully'
            ), 200
    except Exception as e:
        return jsonify(
            status='fail',
            data=[],
            message=str(e)
            ), 400