from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required
from . import customer_bp
from flasgger import swag_from
from .models import Customer
from app.scheduling.models import Appointment, TimeSlot
from app.services.models import Service_Ticket, Service_Ticket_Service, Service
from app.exceptions import ExposedException

#import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

#get all time slots for test drive
@customer_bp.route('/test-drive-time-slots', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get all time slots for test drive',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'time_slot_type',
            'type': 'integer',
            'required': True,
            'description': 'The type of appointment'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of time slots for test drive',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'time_slots': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'time_slot_id': {'type': 'integer'},
                                        'start_time': {'type': 'string'},
                                        'end_time': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request'
        },
        '404': {
            'description': 'Not found'
        }
    }           
})
def get_test_drive_time_slots():
    try:
        test_drive_time_slots = TimeSlot.get_time_slots_by_type(2)
        time_slots = [time_slot.serialize() for time_slot in test_drive_time_slots]
        return standardize_response(data={'time_slots': time_slots}, message='Time slots for test drive retrieved successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to retrieve time slots for test drive', code=400)
    
#get all time slots for service
@customer_bp.route('/service-time-slots', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get all time slots for service',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'time_slot_type',
            'type': 'integer',
            'required': True,
            'description': 'The type of appointment'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of time slots for service',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'time_slots': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'time_slot_id': {'type': 'integer'},
                                        'start_time': {'type': 'string'},
                                        'end_time': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request'
        },
        '404': {
            'description': 'Not found'
        }
    }           
})
def get_service_time_slots():
    try:
        service_time_slots = TimeSlot.get_time_slots_by_type(1)
        time_slots = [time_slot.serialize() for time_slot in service_time_slots]
        return standardize_response(data={'time_slots': time_slots}, message='Time slots for service retrieved successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to retrieve time slots for service', code=400)
    
#create an appointment for test drive
@customer_bp.route('/test-drive-appointment', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Create an appointment for test drive',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'customer_id': {'type': 'integer'},
                    'time_slot_id': {'type': 'integer'},
                    'appointment_type': {'type': 'integer'},
                    'status': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Appointment created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'appointment': {
                                'type': 'object',
                                'properties': {
                                    'appointment_id': {'type': 'integer'},
                                    'appointment_type': {'type': 'integer'},
                                    'time_slot_id': {'type': 'integer'},
                                    'customer_id': {'type': 'integer'},
                                    'status': {'type': 'integer'}
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }           
})
def create_test_drive_appointment():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        time_slot_id = data.get('time_slot_id')
        appointment_type = 2
        status = 3
        appointment = Appointment.create_appointment(customer_id, time_slot_id, appointment_type, status)
        return standardize_response(data={'appointment': appointment.serialize()}, message='Appointment created successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to create appointment', code=400)

#create an appointment for service and create a service ticket

#create an appointment for service
@customer_bp.route('/service-appointment', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Create an appointment for service',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'customer_id': {'type': 'integer'},
                    'time_slot_id': {'type': 'integer'},
                    'appointment_type': {'type': 'integer'},
                    'status': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Appointment created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'appointment': {
                                'type': 'object',
                                'properties': {
                                    'appointment_id': {'type': 'integer'},
                                    'appointment_type': {'type': 'integer'},
                                    'time_slot_id': {'type': 'integer'},
                                    'customer_id': {'type': 'integer'},
                                    'status': {'type': 'integer'}
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }           
})
def create_service_appointment():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        time_slot_id = data.get('time_slot_id')
        appointment_type = 1
        status = 3
        appointment = Appointment.create_appointment(customer_id, time_slot_id, appointment_type, status)
        return standardize_response(data={'appointment': appointment.serialize()}, message='Appointment created successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to create appointment', code=400)
    

#get all appointments by customer_id
@customer_bp.route('/appointments/<int:customer_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get all appointments by customer id',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the customer'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'appointments': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_id': {'type': 'integer'},
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'appointment_type': {'type': 'integer'},
                                        'status': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }           
})
def get_appointments_by_customer_id(customer_id):
    try:
        appointments = Appointment.get_appointments_by_customer_id(customer_id)
        appointments = [appointment.serialize() for appointment in appointments]
        return standardize_response(data={'appointments': appointments}, message='Appointments retrieved successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to retrieve appointments', code=400)


#get all test drive appointments by customer_id
@customer_bp.route('/test-drive-appointments/<int:customer_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get all test drive appointments by customer id',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the customer'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of test drive appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'appointments': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_id': {'type': 'integer'},
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'appointment_type': {'type': 'integer'},
                                        'status': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request'
        },
        '404': {
            'description': 'Not found'
        }
    }           
})
def get_test_drive_appointments_by_customer_id(customer_id):
    try:
        appointments = Appointment.get_all_appointments_by_customer_id_and_appointment_type(customer_id, 2)
        appointments = [appointment.serialize() for appointment in appointments]
        return standardize_response(data={'appointments': appointments}, message='Test drive appointments retrieved successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to retrieve test drive appointments', code=400)

#get all service appointments by customer_id
@customer_bp.route('/service-appointments/<int:customer_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get all service appointments by customer id',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the customer'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of service appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'appointments': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_id': {'type': 'integer'},
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'appointment_type': {'type': 'integer'},
                                        'status': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request'
        },
        '404': {
            'description': 'Not found'
        }
    }           
})
def get_service_appointments_by_customer_id(customer_id):
    try:
        appointments = Appointment.get_all_appointments_by_customer_id_and_appointment_type(customer_id, 1)
        appointments = [appointment.serialize() for appointment in appointments]
        return standardize_response(data={'appointments': appointments}, message='Service appointments retrieved successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to retrieve service appointments', code=400)

#cancel test drive appointment by appointment_id
@customer_bp.route('/test-drive-appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'summary': 'Cancel a test drive appointment by customer',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the appointment'
        }
    ],
    'responses': {
        '200': {
            'description': 'Test drive appointment cancelled successfully'
        },
        '400': {
            'description': 'Bad request'
        },
        '404': {
            'description': 'Not found'
        }
    }           
})
def cancel_test_drive_appointment(appointment_id):
    try:
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if appointment.appointment_type != 2:
            raise ExposedException('This is not a test drive appointment')
        if appointment.status == 2:
            raise ExposedException('This appointment has already been cancelled')
        appointment.status = 2
        appointment.save()
        return standardize_response(message='Test drive appointment cancelled successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to cancel test drive appointment', code=400)
    
#cancel service appointment by appointment_id
@customer_bp.route('/service-appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'summary': 'Cancel a service appointment by customer',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the appointment'
        }
    ],
    'responses': {
        '200': {
            'description': 'Service appointment cancelled successfully'
        },
        '400': {
            'description': 'Bad request'
        },
        '404': {
            'description': 'Not found'
        }
    }           
})
def cancel_service_appointment(appointment_id):
    try:
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if appointment.appointment_type != 1:
            raise ExposedException('This is not a service appointment')
        if appointment.status == 2:
            raise ExposedException('This appointment has already been cancelled')
        appointment.status = 2
        appointment.save()
        return standardize_response(message='Service appointment cancelled successfully', code = 200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(message=str(e), code=400)
        return standardize_response(message='Failed to cancel service appointment', code=400)