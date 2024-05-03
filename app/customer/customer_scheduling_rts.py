from flask import jsonify, request, g, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import customer_bp
from flasgger import swag_from
from .models import Customer
from app.scheduling.models import Appointment, TimeSlot, Service_Ticket, Service_Ticket_Service
from app.inventory.models import Service
from app.exceptions import ExposedException
from flasgger import swag_from

#import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

#schedule a test drive
@customer_bp.route('/appointment/test-drive', methods=['POST'])
@swag_from({
    'summary': 'Schedule a test drive',
    'tags': ['Customer Scheduling'],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_id': {'type': 'integer'},
                        'time_slot_id': {'type': 'integer'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Test drive scheduled successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'appointment_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }
})
def schedule_test_drive():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        time_slot_id = data.get('time_slot_id')
        appointment_id = g.scheduling_service.schedule_test_drive(customer_id=customer_id, time_slot_id=time_slot_id)
        return standardize_response(data=appointment_id, message='Test drive scheduled successfully', code = 201)
    except Exception as e:
        raise e
    
#schedule a service
@customer_bp.route('/appointment/service', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Schedule a service',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_id': {'type': 'integer'},
                        'time_slot_id': {'type': 'integer'},
                        'customer_vehicle_id': {'type': 'integer'},
                        'customer_note': {'type': 'string', 'example': 'No notes added...'},
                        'technician_note': {'type': 'string', 'example': 'No notes added...'},
                        'services': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'service_id': {'type': 'integer'},
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Service scheduled successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'appointment_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }
})
def schedule_service():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        time_slot_id = data.get('time_slot_id')
        customer_vehicle_id = data.get('customer_vehicle_id')
        customer_note = data.get('customer_note')
        technician_note = data.get('technician_note')
        services = data.get('services')
        service_ticket_id = g.scheduling_service.schedule_service(customer_id=customer_id, time_slot_id=time_slot_id, customer_vehicle_id=customer_vehicle_id, customer_note=customer_note, technician_note=technician_note, services=services)
        return standardize_response(data=service_ticket_id, message='Service scheduled successfully', code = 201)
    except Exception as e:
        raise e


#cancel appointment
@customer_bp.route('/appointment/<int:appointment_id>/cancel', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Cancel an appointment',
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
            'description': 'Appointment cancelled successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'appointment_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }
})
def cancel_appointment(appointment_id):
    try:
        g.scheduling_service.cancel_appointment(appointment_id)
        return standardize_response(data=appointment_id, message='Appointment cancelled successfully', code = 201)
    except Exception as e:
        raise e

#get appointments by customer_id
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
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'appointment_id': {'type': 'integer'},
                                'customer': {
                                    'type': 'object',
                                    'properties': {
                                        'customer_id': {'type': 'integer'},
                                        'first_name': {'type': 'string'},
                                        'last_name': {'type': 'string'}
                                    }
                                },
                                'customer_id': {'type': 'integer'},
                                'time_slot': {
                                    'type': 'object',
                                    'properties': {
                                        'start_time': {'type': 'DateTime'},
                                        'end_time': {'type': 'DateTime'}
                                    }
                                },
                                'time_slot_id': {'type': 'integer'},
                                'appointment_type': {'type': 'integer'},
                                'status': {'type': 'integer'}
                            }
                        }
                    },
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        },
        '404': {
            'description': 'No appointments found'
        },
        '400': {
            'description': 'Bad request'
        }
    }
})
def get_appointments_by_customer_id(customer_id):
    try:
        appointments = g.scheduling_service.get_appointments_by_customer_id(customer_id)
        return standardize_response(data=appointments, message='Appointments retrieved successfully', code = 200)
    except Exception as e:
        raise e


#add customer notes to service ticket
@customer_bp.route('/service-ticket/<int:service_ticket_id>/customer-notes', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Add customer notes to service ticket',
    'tags': ['Customer Scheduling'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'service_ticket_id',
            'type': 'integer',
            'required': True,
            'description': 'The id of the service ticket'
        }
    ],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'customer_note': {'type': 'string', 'example': 'No notes added...'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Customer notes added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'data': {'type': 'string', 'description': 'Customer notes added successfully'},
                    'message': {'type': 'string', 'description': 'Status message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        },
        '400': {
            'description': 'Bad request',
            'schema' : {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'data': {'type': 'string', 'description': 'Bad request'},
                    'message': {'type': 'string', 'description': 'Status message'},
                    'code': {'type': 'integer', 'description': 'HTTP status code'}
                }
            }
        }
    }
})
def add_customer_note_to_service_ticket(service_ticket_id):
    try:
        data = request.get_json()
        customer_note = data.get('customer_note')
        customer_note = g.scheduling_service.add_customer_note(customer_note=customer_note, service_ticket_id=service_ticket_id)
        return standardize_response(data=customer_note, message='Customer notes added successfully', code = 201)
    except Exception as e:
        raise e

