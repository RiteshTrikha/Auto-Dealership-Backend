from flask import jsonify, request, current_app, g
from flask_jwt_extended import jwt_required
from . import user_bp
from flasgger import swag_from
from app.scheduling.models import Appointment, TimeSlot, Service, Service_Ticket, Service_Ticket_Service
from app.exceptions import ExposedException
from app.auth.auth_decorators import user_required, manager_required

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

#get all appointments
@user_bp.route('/appointments', methods=['GET'], endpoint='get_all_appointments_for_user')
@swag_from({
    'summary': 'Get all appointments',
    'tags': ['User Scheduling'],
    'security': [{'BearerAuth': []}],
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
        }
    }
})
@jwt_required()
@user_required
def get_all_appointments():
    try:
        appointments = g.scheduling_service.get_all_appointments()
        if isinstance(appointments, list):
            appointments = [str(appointment) if isinstance(appointment, int) else appointment for appointment in appointments]
        elif isinstance(appointments, dict):
          for key in appointments:
              if isinstance(appointments[key], int):
                  appointments[key] = str(appointments[key]) 
        if appointments == []:
            return standardize_response(status= 'fail', data=None, message='No appointments found', code = 404)
        return standardize_response(status='success', data=appointments, message='Appointments retrieved successfully', code = 200)
    except Exception as e:
        raise e
    
# get all test drive appointments
@user_bp.route('/appointments/test_drive', methods=['GET'], endpoint='get_test_drive_appointments')
@jwt_required()
@user_required
@swag_from({
    'summary': 'Get all test drive appointments',
    'tags': ['User Scheduling'],
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {
            'description': 'A list of test drive appointments',
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
        }
    }
})
def get_test_drive_appointments():
    try:
        appointments = g.scheduling_service.get_test_drive_appointments()
        if isinstance(appointments, list):
            appointments = [str(appointment) if isinstance(appointment, int) else appointment for appointment in appointments]
        elif isinstance(appointments, dict):
            for key in appointments:
                if isinstance(appointments[key], int):
                    appointments[key] = str(appointments[key])
        if appointments == []:
            return standardize_response(status= 'fail', data=None, message='No test drive appointments found', code = 404)
        return standardize_response(data=appointments, message='Test drive appointments retrieved successfully', code = 200)
    except Exception as e:
        raise e

# get all service appointments
@user_bp.route('/appointments/service', methods=['GET'], endpoint='get_service_appointments')
@jwt_required()
@user_required
@swag_from({
    'summary': 'Get all service appointments',
    'tags': ['User Scheduling'],
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {
            'description': 'A list of service appointments',
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
        }
    }
})
def get_service_appointments():
    try:
        appointments = g.scheduling_service.get_service_appointments()
        if isinstance(appointments, list):
            appointments = [str(appointment) if isinstance(appointment, int) else appointment for appointment in appointments]
        elif isinstance(appointments, dict):
            for key in appointments:
                if isinstance(appointments[key], int):
                    appointments[key] = str(appointments[key])
        if appointments == []:
            return standardize_response(status= 'fail', data=None, message='No service appointments found', code = 404)
        return standardize_response(data=appointments, message='Service appointments retrieved successfully', code = 200)
    except Exception as e:
        raise e
    
#get all appoinntments with service tickets
@user_bp.route('/appointments/service_tickets', methods=['GET'], endpoint='get_all_appointments_with_service_ticket')
@jwt_required()
@user_required
@swag_from({
    'summary': 'Get all appointments with service tickets',
    'tags': ['User Scheduling'],
    'security': [{'BearerAuth': []}],
    'responses': {
        '200': {
            'description': 'A list of service appointments with service tickets',
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
                                'appointment_type': {'type': 'string'},
                                'status': {'type': 'string'},
                                'service_ticket': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'service_ticket_id': {'type': 'integer'},
                                            'customer_id': {'type': 'integer'},
                                            'user_id': {'type': 'integer'},
                                            'customer_vehical_id': {'type': 'integer'},
                                            'time_slot_id': {'type': 'integer'},
                                            'customer_note': {'type': 'string'},
                                            'technician_note': {'type': 'string'},
                                            'status': {'type': 'string'}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'message': {'type': 'string'},
                    'code': {'type': 'integer'}
                }
            }
        }
    }
})
def get_all_appointments_with_service_ticket():
    try:
        appointments = g.scheduling_service.get_all_appointments_with_service_ticket()
        if isinstance(appointments, list):
            appointments = [str(appointment) if isinstance(appointment, int) else appointment for appointment in appointments]
        elif isinstance(appointments, dict):
            for key in appointments:
                if isinstance(appointments[key], int):
                    appointments[key] = str(appointments[key])
        if appointments == []:
            return standardize_response(status= 'fail', data=None, message='No service appointments with service tickets found', code = 404)
        return standardize_response(data=appointments, message='Appointments with service tickets retrieved successfully', code = 200)
    except Exception as e:
        raise e


#cancel appointment
@user_bp.route('/appointment/<int:appointment_id>/cancel', methods=['POST'], endpoint='cancel_appointment')
@jwt_required()
@manager_required
@swag_from({
    'summary': 'Cancel an appointment',
    'tags': ['User Scheduling'],
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
        return standardize_response(status='success' ,data=None, message='Appointment cancelled successfully', code = 201)
    except Exception as e:
        raise e
    
# update appointment status to confirmed
@user_bp.route('/appointment/<int:appointment_id>/confirm', methods=['POST'], endpoint='confirm_appointment')
@jwt_required()
@manager_required
@swag_from({
    'summary': 'Confirm an appointment',
    'tags': ['User Scheduling'],
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
            'description': 'Appointment confirmed successfully',
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
def confirm_appointment(appointment_id):
    try:
        g.scheduling_service.confirm_appointment(appointment_id)
        return standardize_response(status='success', data=None, message='Appointment confirmed successfully', code = 201)
    except Exception as e:
        raise e
    
# assign technician to service ticket
@user_bp.route('/service_ticket/<int:service_ticket_id>/assign_technician', methods=['POST'], endpoint='assign_technician_to_service_ticket')
@jwt_required()
@manager_required
@swag_from({
    'summary': 'Assign a technician to a service ticket',
    'tags': ['User Scheduling'],
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
                        'user_id': {'type': 'integer'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Technician assigned to service ticket successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'data': {'type': 'string', 'description': 'Technician was assigned successfully'},
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
def assign_technician_to_service_ticket(service_ticket_id):
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id or not isinstance(user_id, int):
            return standardize_response(status='fail', data=None, message='User id is invalid', code = 400)
        g.scheduling_service.assign_technician(service_ticket_id, user_id=user_id)
        return standardize_response(status='success', data=None, message='Technician assigned to service ticket successfully', code = 201)
    except Exception as e:
        raise e
    
# add technician notes to service ticket
@user_bp.route('/service_ticket/<int:service_ticket_id>/add_technician_note', methods=['POST'], endpoint='add_technician_note_to_service_ticket')
@jwt_required()
@user_required
@swag_from({
    'summary': 'Add technician notes to a service ticket',
    'tags': ['User Scheduling'],
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
                        'technician_note': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Technician notes added to service ticket successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Request status'},
                    'data': {'type': 'string', 'description': 'Technician notes added successfully'},
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
def add_technician_note_to_service_ticket(service_ticket_id):
    try:
        data = request.get_json()
        technician_note = data.get('technician_note')
        g.scheduling_service.add_technician_note(technician_note=technician_note, service_ticket_id=service_ticket_id)
        return standardize_response(status='success', data=None, message='Technician notes added to service ticket successfully', code = 201)
    except Exception as e:
        raise e
    
#Update service ticket status to closed
@user_bp.route('/service_ticket/<int:service_ticket_id>/close', methods=['POST'], endpoint='close_service_ticket')
@jwt_required()
@user_required
@swag_from({
    'summary': 'Close a service ticket',
    'tags': ['User Scheduling'],
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
    'responses': {
        '200': {
            'description': 'Service ticket closed successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'service_ticket_id': {'type': 'integer'}
                }
            }
        },
        '400': {
            'description': 'Bad request'
        }
    }
})
def close_service_ticket(service_ticket_id):
    try:
        g.scheduling_service.close_service_ticket(service_ticket_id)
        return standardize_response(data=service_ticket_id, message='Service ticket closed successfully', code = 201)
    except Exception as e:
        raise e
