from flask import jsonify, request, current_app
from . import scheduling_bp
from .models import *
from app.exceptions import ExposedException
from flasgger import swag_from

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response
#reminder:
#NEED TO MOVE THE THESE ROUTES TO EITHER CUSTOMER OR USER OR LEAVE IT HERE
#ALSO NOT ALL OF THESE WILL BE USED

# get all time slots
@scheduling_bp.route('/time-slots', methods=['GET'])
@swag_from({
    'summary': 'Get all time slots',
    'tags': ['Scheduling'],
    'responses': {
        '200': {
            'description': 'A list of time slots',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'time_slot_id': {'type': 'integer'},
                                        'start_time': {'type': 'datetime'},
                                        'end_time': {'type': 'datetime'},
                                        'time_slot_type': {'type': 'integer'},
                                        'is_available': {'type': 'integer'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving time slots',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No time slots found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_all_time_slots():
    try:
        time_slots = TimeSlot.get_all_time_slots()
        if time_slots is None:
            return standardize_response(status='fail', data=[], message='No time slots found', code=404)
        return standardize_response(status='success', data=[time_slot.serialize() for time_slot in time_slots],
                                    message='Time slots retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving time slots', code=400)

# get all available time slots
@scheduling_bp.route('/time-slots/availability/<is_available>', methods=['GET'])
@swag_from({
    'summary': 'Get available time slots',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'is_available',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The availability of time slot'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of available time slots',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'time_slot_id': {'type': 'integer'},
                                        'start_time': {'type': 'datetime'},
                                        'end_time': {'type': 'datetime'},
                                        'time_slot_type': {'type': 'integer'},
                                        'is_available': {'type': 'integer'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving available time slots',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No available time slots',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
    }
)

def get_available_time_slots():
    try:
        time_slots = TimeSlot.get_available_time_slots()
        if time_slots is None:
            return standardize_response(status='fail', data=[], message='No available time slots', code=404)
        return standardize_response(status='success', data=[time_slot.serialize() for time_slot in time_slots],
                                    message='Available time slots retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving available time slots', code=400)

#get time slot by type and availability
@scheduling_bp.route('/time-slots/type/<time_slot_type>/availability/<is_available>', methods=['GET'])
@swag_from({
    'summary': 'Get time slots by type and availability',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'time_slot_type',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The type of time slot'
        },
        {
            'in': 'path',
            'name': 'is_available',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The availability of time slot'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of time slots',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'time_slot_id': {'type': 'integer'},
                                        'start_time': {'type': 'datetime'},
                                        'end_time': {'type': 'datetime'},
                                        'time_slot_type': {'type': 'integer'},
                                        'is_available': {'type': 'integer'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving time slots by type and availability',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No time slots found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_time_slot_by_type_and_availability(time_slot_type, is_available):
    try:
        time_slots = TimeSlot.get_time_slot_by_type_and_availability(time_slot_type, is_available)
        if time_slots is None:
            return standardize_response(status='fail', data=[], message='No time slots found', code=404)
        return standardize_response(status='success', data=[time_slot.serialize() for time_slot in time_slots],
                                    message='Time slots retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving time slots by type and availability', code=400)

#get time slot by type
@scheduling_bp.route('/time-slots/type/<time_slot_type>', methods=['GET'])
@swag_from({
    'summary': 'Get time slots by type',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'time_slot_type',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The type of time slot'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of time slots',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'time_slot_id': {'type': 'integer'},
                                        'start_time': {'type': 'datetime'},
                                        'end_time': {'type': 'datetime'},
                                        'time_slot_type': {'type': 'integer'},
                                        'is_available': {'type': 'integer'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving time slots by type',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No time slots found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_time_slot_by_type(time_slot_type):
    try:
        time_slots = TimeSlot.get_time_slot_by_type(time_slot_type)
        if time_slots is None:
            return standardize_response(status='fail', data=[], message='No time slots found', code=404)
        return standardize_response(status='success', data=[time_slot.serialize() for time_slot in time_slots],
                                    message='Time slots retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving time slots by type', code=400)

#get time slot by time slot id
@scheduling_bp.route('/time-slots/<time_slot_id>', methods=['GET'])
@swag_from(
    {
    'summary': 'Get time slot by time slot id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'time_slot_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the time slot'
        }
    ],
    'responses': {
        '200': {
            'description': 'The time slot',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'time_slot_id': {'type': 'integer'},
                                    'start_time': {'type': 'datetime'},
                                    'end_time': {'type': 'datetime'},
                                    'time_slot_type': {'type': 'integer'},
                                    'is_available': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving time slot',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Time slot not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
    }
)
def get_time_slot(time_slot_id):
    try:
        time_slot = TimeSlot.get_time_slot_by_id(time_slot_id)
        if time_slot is None:
            return standardize_response(status='fail', data=[], message='Time slot not found', code=404)
        return standardize_response(status='success', data=time_slot.serialize(),
                                    message='Time slot retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message=str(e), code=400)
    
#Create time slot
@scheduling_bp.route('/time-slots', methods=['POST'])
@swag_from(
    {
        'summary': 'Create time slot',
        'tags': ['Scheduling'],
        'parameters': [
            {
                'in': 'body',
                'name': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'time_slot_id': {'type': 'integer'},
                        'start_time': {'type': 'string'},
                        'end_time': {'type': 'string'},
                        'time_slot_type': {'type': 'integer'},
                        'is_available': {'type': 'integer'}
                    }
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'The created time slot',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': {'type': 'string'},
                                'data': {
                                    'type': 'object',
                                    'properties': {
                                        'time_slot_id': {'type': 'integer'},
                                        'start_time': {'type': 'datetime'},
                                        'end_time': {'type': 'datetime'},
                                        'time_slot_type': {'type': 'integer'},
                                        'is_available': {'type': 'integer'}
                                    }
                                },
                                'message': {'type': 'string'},
                                'code': {'type': 'integer'}
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'An error occurred while creating time slot',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': {'type': 'string'},
                                'message': {'type': 'string'},
                                'code': {'type': 'integer'}
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'Time slot not found',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': {'type': 'string'},
                                'data': {'type': 'array'},
                                'message': {'type': 'string'},
                                'code': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
)

def create_time_slot():
    try:
        data = request.get_json()
        time_slot_id = data['time_slot_id']
        start_time = data['start_time']
        end_time = data['end_time']
        time_slot_type = data['time_slot_type']
        is_available = data['is_available']
        time_slot = TimeSlot.create_time_slot(time_slot_id, start_time, end_time, time_slot_type, is_available)
        return standardize_response(status='success', data={'time_slot_id': time_slot_id},
                                    message='Time slot created successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message=str(e), code=400)
    
#Update time slot
@scheduling_bp.route('/time-slots/<time_slot_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update time slot by time slot id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'time_slot_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the time slot'
        }
    ],
    'responses': {
        '200': {
            'description': 'The updated time slot',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'time_slot_id': {'type': 'integer'},
                                    'start_time': {'type': 'datetime'},
                                    'end_time': {'type': 'datetime'},
                                    'time_slot_type': {'type': 'integer'},
                                    'is_available': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while updating time slot',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Time slot not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def update_time_slot(time_slot_id):
    try:
        data = request.get_json()
        time_slot = TimeSlot.update_time_slot(time_slot_id, data)
        if time_slot is None:
            return standardize_response(status='fail', data=[], message='Time slot not found', code=404)
        return standardize_response(status='success', data=time_slot.serialize(),
                                    message='Time slot updated successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message=str(e), code=400)

####################################################################################################################
# get all appointments
@scheduling_bp.route('/appointments', methods=['GET'])
@swag_from({
    'summary': 'Get all appointments',
    'tags': ['Scheduling'],
    'responses': {
        '200': {
            'description': 'A list of appointments',
            'content': {
                'application/json': {
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
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'user_id': {'type': 'integer'},
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
        },
        '400': {
            'description': 'An error occurred while retrieving appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404':
            {
                'description': 'No appointments found',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': {'type': 'string'},
                                'data': {'type': 'array'},
                                'message': {'type': 'string'},
                                'code': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
    }
})
def get_all_appointments():
    try:
        appointments = Appointment.get_all_appointments()
        return standardize_response(status='success', data=[appointment.serialize() for appointment in appointments],
                                    message='Appointments retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving appointments', code=400)
    
#get all appointments by appointment id
@scheduling_bp.route('/appointments/<appointment_id>', methods=['GET'])
@swag_from({
    'summary': 'Get appointment by appointment id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the appointment'
        }
    ],
    'responses': {
        '200': {
            'description': 'The appointment',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'appointment_id': {'type': 'integer'},
                                    'time_slot_id': {'type': 'integer'},
                                    'customer_id': {'type': 'integer'},
                                    'user_id': {'type': 'integer'},
                                    'appointment_type': {'type': 'integer'},
                                    'status': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving appointment',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_appointment(appointment_id):
    try:
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if appointment is None:
            return standardize_response(status='fail', data=[], message='Appointment not found', code=404)
        return standardize_response(status='success', data=appointment.serialize(),
                                    message='Appointment retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message=str(e), code=400)
    
#get appointment by user id
@scheduling_bp.route('/appointments/user/<user_id>', methods=['GET'])
@swag_from({
    'summary': 'Get appointment by user id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the user'
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
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_id': {'type': 'integer'},
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'user_id': {'type': 'integer'},
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
        },
        '400': {
            'description': 'An error occurred while retrieving appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No appointments found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_appointment_by_user_id(user_id):
    try:
        appointments = Appointment.get_appointment_by_user_id(user_id)
        return standardize_response(status='success', data=[appointment.serialize() for appointment in appointments],
                                    message='Appointments retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving appointments', code=400)
    
#get appointment by customer id
@scheduling_bp.route('/appointments/customer/<customer_id>', methods=['GET'])
@swag_from({
    'summary': 'Get appointment by customer id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_id',
            'schema': {
                'type': 'integer'
            },
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
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_id': {'type': 'integer'},
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'user_id': {'type': 'integer'},
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
        },
        '400': {
            'description': 'An error occurred while retrieving appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No appointments found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_appointment_by_customer_id(customer_id):
    try:
        appointments = Appointment.get_appointment_by_customer_id(customer_id)
        return standardize_response(status='success', data=[appointment.serialize() for appointment in appointments],
                                    message='Appointments retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving appointments', code=400)    
    
#Get all appointments by appointment type
@scheduling_bp.route('/appointments/appointment_type/<appointment_type>', methods=['GET'])
@swag_from({
    'summary': 'Get appointments by appointment type',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_type',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The type of appointment'
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
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_id': {'type': 'integer'},
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'user_id': {'type': 'integer'},
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
        },
        '400': {
            'description': 'An error occurred while retrieving appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No appointments found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_all_appointments_by_appointment_type(appointment_type):
    try:
        appointments = Appointment.get_all_appointments_by_appointment_type(appointment_type)
        return standardize_response(status='success', data=[appointment.serialize() for appointment in appointments],
                                    message='Appointments retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving appointments', code=400)

#get appointments by time slot id
@scheduling_bp.route('/appointments/time-slot/<time_slot_id>', methods=['GET'])
@swag_from({
    'summary': 'Get appointments by time slot id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'time_slot_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the time slot'
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
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_id': {'type': 'integer'},
                                        'time_slot_id': {'type': 'integer'},
                                        'customer_id': {'type': 'integer'},
                                        'user_id': {'type': 'integer'},
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
        },
        '400': {
            'description': 'An error occurred while retrieving appointments',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'No appointments found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_appointments_by_time_slot_id(time_slot_id):
    try:
        appointments = Appointment.get_appointments_by_time_slot_id(time_slot_id)
        return standardize_response(status='success', data=[appointment.serialize() for appointment in appointments],
                                    message='Appointments retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving appointments', code=400)

#Create appointment
@scheduling_bp.route('/appointments', methods=['POST'])
@swag_from({
    'summary': 'Create appointment',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'time_slot_id': {'type': 'integer'},
                    'customer_id': {'type': 'integer'},
                    'user_id': {'type': 'integer'},
                    'appointment_type': {'type': 'integer'},
                    'status': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'The created appointment',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'appointment_id': {'type': 'integer'},
                                    'time_slot_id': {'type': 'integer'},
                                    'customer_id': {'type': 'integer'},
                                    'user_id': {'type': 'integer'},
                                    'appointment_type': {'type': 'integer'},
                                    'status': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while creating appointment',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
    })
def create_appointment():
    try:
        data = request.get_json()
        appointment = Appointment.create_appointment(data)
        return standardize_response(status='success', data=appointment.serialize(),
                                    message='Appointment created successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message=str(e), code=400)
    
#Update appointment status
@scheduling_bp.route('/appointments/<appointment_id>/status', methods=['PUT'])
@swag_from({
    'summary': 'Update appointment status by appointment id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the appointment'
        }
    ],
    'responses': {
        '200': {
            'description': 'The updated appointment status',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'appointment_id': {'type': 'integer'},
                                    'time_slot_id': {'type': 'integer'},
                                    'customer_id': {'type': 'integer'},
                                    'user_id': {'type': 'integer'},
                                    'appointment_type': {'type': 'integer'},
                                    'status': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while updating appointment status',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def update_appointment_status(appointment_id):
    try:
        data = request.get_json()
        appointment = Appointment.update_appointment_status(appointment_id, data)
        if appointment is None:
            return standardize_response(status='fail', data=[], message='Appointment not found', code=404)
        return standardize_response(status='success', data=appointment.serialize(),
                                    message='Appointment status updated successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message=str(e), code=400)

####################################################################################################################
        
#get all appointment details
@scheduling_bp.route('/appointment-details', methods=['GET'])
@swag_from({
    'summary': 'Get all appointment details',
    'tags': ['Scheduling'],
    'responses': {
        '200': {
            'description': 'A list of appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_details_id': {'type': 'integer'},
                                        'appointment_id': {'type': 'integer'},
                                        'customer_vehical_id': {'type': 'integer'},
                                        'customer_message': {'type': 'string'},
                                        'notes': {'type': 'string'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404':{
                'description': 'No appointment details found',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': {'type': 'string'},
                                'data': {'type': 'array'},
                                'message': {'type': 'string'},
                                'code': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
    }   
})
def get_all_appointment_details():
    try:
        appointment_details = AppointmentDetail.get_all_appointment_details()
        return standardize_response(status='success', data=[appointment_detail.serialize() for appointment_detail in appointment_details],
                                    message='Appointment details retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message='An error occurred while retrieving appointment details', code=400)


# get appointment details by appointment id
@scheduling_bp.route('/appointments/<appointment_id>/appointment-details', methods=['GET'])
@swag_from({
    'summary': 'Get appointment details by appointment id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the appointment'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_details_id': {'type': 'integer'},
                                        'appointment_id': {'type': 'integer'},
                                        'customer_vehical_id': {'type': 'integer'},
                                        'customer_message': {'type': 'string'},
                                        'notes': {'type': 'string'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment details not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_appointment_details_by_appointment_id(appointment_id):
    try:
        appointment_details = AppointmentDetail.get_appointment_details_by_appointment_id(appointment_id)
        if appointment_details == []:
            return standardize_response(status='fail', data=[], message='Appointment details not found', code=404)
        return standardize_response(status='success', data=[appointment_detail.serialize() for appointment_detail in appointment_details],
                                    message='Appointment details retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error retrieving appointment details", code=400)

# get appointment details by appointment details id
@scheduling_bp.route('/appointment-details/<appointment_details_id>', methods=['GET'])
@swag_from({
    'summary': 'Get appointment details by appointment details id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_details_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the appointment details'
        }
    ],
    'responses': {
        '200': {
            'description': 'The appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'appointment_details_id': {'type': 'integer'},
                                    'appointment_id': {'type': 'integer'},
                                    'customer_vehical_id': {'type': 'integer'},
                                    'customer_message': {'type': 'string'},
                                    'notes': {'type': 'string'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment details not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }   
})
def get_appointment_detail(appointment_details_id):
    try:
        appointment_details = AppointmentDetail.get_appointment_details_by_appointment_details_id(appointment_details_id)
        if appointment_details is None:
            return standardize_response(status='fail', data=[], message='Appointment details not found', code=404)
        return standardize_response(status='success', data=appointment_details.serialize(),
                                    message='Appointment details retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error retrieving appointment details", code=400)

#Get appoinment details by customer vehicle id
@scheduling_bp.route('/appointment-details/customer-vehicle/<customer_vehicle_id>', methods=['GET'])
@swag_from({
    'summary': 'Get appointment details by customer vehicle id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'customer_vehicle_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the customer vehicle'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'appointment_details_id': {'type': 'integer'},
                                        'appointment_id': {'type': 'integer'},
                                        'customer_vehical_id': {'type': 'integer'},
                                        'customer_message': {'type': 'string'},
                                        'notes': {'type': 'string'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while retrieving appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment details not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_appointment_details_by_customer_vehicle_id(customer_vehicle_id):
    try:
        appointment_details = AppointmentDetail.get_appointment_details_by_customer_vehicle_id(customer_vehicle_id)
        if appointment_details is None:
            return standardize_response(status='fail', data=[], message='Appointment details not found', code=404)
        return standardize_response(status='success', data=[appointment_detail.serialize() for appointment_detail in appointment_details],
                                    message='Appointment details retrieved successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error retrieving appointment details", code=400)

#Create appointment details
@scheduling_bp.route('/appointment-details', methods=['POST'])
@swag_from({
    'summary': 'Create appointment details',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'appointment_id': {'type': 'integer'},
                    'customer_vehical_id': {'type': 'integer'},
                    'customer_message': {'type': 'string'},
                    'notes': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'The created appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'appointment_details_id': {'type': 'integer'},
                                    'appointment_id': {'type': 'integer'},
                                    'customer_vehical_id': {'type': 'integer'},
                                    'customer_message': {'type': 'string'},
                                    'notes': {'type': 'string'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while creating appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment details not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def create_appointment_detail():
    try:
        data = request.get_json()
        appointment_details = AppointmentDetail.create_appointment_details(data)
        return standardize_response(status='success', data=appointment_details.serialize(),
                                    message='Appointment details created successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        if isinstance(e, ExposedException):
            return standardize_response(status='fail', message=str(e), code=400)
        return standardize_response(status='fail', message="Error creating appointment details", code=400)

#Update appointment details
@scheduling_bp.route('/appointment-details/<appointment_details_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update appointment details by appointment details id',
    'tags': ['Scheduling'],
    'parameters': [
        {
            'in': 'path',
            'name': 'appointment_details_id',
            'schema': {
                'type': 'integer'
            },
            'required': True,
            'description': 'The id of the appointment details'
        }
    ],
    'responses': {
        '200': {
            'description': 'The updated appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'appointment_details_id': {'type': 'integer'},
                                    'appointment_id': {'type': 'integer'},
                                    'customer_vehical_id': {'type': 'integer'},
                                    'customer_message': {'type': 'string'},
                                    'notes': {'type': 'string'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'An error occurred while updating appointment details',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Appointment details not found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'data': {'type': 'array'},
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def update_appointment_detail(appointment_details_id):
    try:
        data = request.get_json()
        appointment_details = AppointmentDetail.update_appointment_details(appointment_details_id, data)
        if appointment_details is None:
            return standardize_response(status='fail', data=[], message='Appointment details not found', code=404)
        return standardize_response(status='success', data=appointment_details.serialize(),
                                    message='Appointment details updated successfully', code=200)
    except Exception as e:
        current_app.logger.error(str(e))
        return standardize_response(status='fail', message=str(e), code=400)