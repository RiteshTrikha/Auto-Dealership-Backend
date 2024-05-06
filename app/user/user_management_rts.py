from flask import jsonify, request, current_app, g
from . import user_bp
from .models import User
from .services import UserServices
from app.exceptions import ExposedException
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from app.auth.auth_decorators import manager_required

# import utilities
from app.utilities import Utilities
standardize_response = Utilities.standardize_response

# user management routes

# get all users
@user_bp.route('/management/users', methods=['GET'])
@swag_from({
    'summary': 'Get all users',
    'tags': ['User Management'],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'Users fetched successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'user_id': {'type': 'integer'},
                                        'email': {'type': 'string'},
                                        'first_name': {'type': 'string'},
                                        'last_name': {'type': 'string'},
                                        'role_id': {'type': 'integer'},
                                        'role': {'type': 'string'},
                                        'is_active': {'type': 'integer'}
                                    }
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def get_all_users():
    try:
        users_dict = UserServices().get_all()
        return standardize_response(data=users_dict, message='Users fetched successfully', code=200)
    except Exception as e:
        raise e

# get user by id
@user_bp.route('/management/user/<int:user_id>', methods=['GET'])
@swag_from({
    'summary': 'Get user by id',
    'tags': ['User Management'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'required': True,
            'description': 'User ID',
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'User fetched successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'user_id': {'type': 'integer'},
                                    'email': {'type': 'string'},
                                    'first_name': {'type': 'string'},
                                    'last_name': {'type': 'string'},
                                    'role_id': {'type': 'integer'},
                                    'role': {'type': 'string'},
                                    'is_active': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def get_user(user_id):
    try:
        user_dict = UserServices().get_by_id(user_id)
        return standardize_response(data=user_dict, message='User fetched successfully', code=200)
    except Exception as e:
        raise e

# create user
@user_bp.route('/management/user', methods=['POST'])
@swag_from({
    'summary': 'Create user',
    'tags': ['User Management'],
    'security': [{'BearerAuth': []}],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {'type': 'string'},
                        'password': {'type': 'string'},
                        'first_name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'role_id': {'type': 'integer', 'example': 1}
                    }
                }
            }
        }
    },
    'responses': {
        201: {
            'description': 'User created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'user_id': {'type': 'integer'},
                                    'email': {'type': 'string'},
                                    'first_name': {'type': 'string'},
                                    'last_name': {'type': 'string'},
                                    'role_id': {'type': 'integer'},
                                    'role': {'type': 'string'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def create_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role_id = data.get('role_id')
        
        dict = UserServices().create_user(email=email, password=password, first_name=first_name, last_name=last_name, role_id=role_id)

        return standardize_response(data=dict, message='User created successfully', code=201)
    except Exception as e:
        raise e
    
# update user
@user_bp.route('/management/user/<int:user_id>', methods=['PUT'])
@swag_from({
    'summary': 'Update user',
    'tags': ['User Management'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'required': True,
            'description': 'User ID',
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {'type': 'string'},
                        'password': {'type': 'string'},
                        'first_name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'role_id': {'type': 'integer', 'example': 1}
                    }
                }
            }
        }
    },
    'responses': {
        200: {
            'description': 'User updated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'user_id': {'type': 'integer'},
                                    'email': {'type': 'string'},
                                    'first_name': {'type': 'string'},
                                    'last_name': {'type': 'string'},
                                    'role_id': {'type': 'integer'},
                                    'role': {'type': 'string'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def update_user(user_id):
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role_id = data.get('role_id')
        
        dict = UserServices().update_user(user_id=user_id, email=email, password=password, 
                                          first_name=first_name, last_name=last_name, role_id=role_id)

        return standardize_response(data=dict, message='User updated successfully', code=200)
    except Exception as e:
        raise e
    
# deactivate user
@user_bp.route('/management/user/deactivate/<int:user_id>', methods=['PUT'])
@swag_from({
    'summary': 'Deactivate user',
    'tags': ['User Management'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'required': True,
            'description': 'User ID',
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'User deactivated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'user_id': {'type': 'integer'},
                                    'is_active': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def deactivate_user(user_id):
    try:
        dict = UserServices().deactivate_user(user_id=user_id)

        return standardize_response(data=dict, message='User deactivated successfully', code=200)
    except Exception as e:
        raise e
    
# activate user
@user_bp.route('/management/user/activate/<int:user_id>', methods=['PUT'])
@swag_from({
    'summary': 'Activate user',
    'tags': ['User Management'],
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'in': 'path',
            'name': 'user_id',
            'required': True,
            'description': 'User ID',
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'User activated successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'data': {
                                'type': 'object',
                                'properties': {
                                    'user_id': {'type': 'integer'},
                                    'is_active': {'type': 'integer'}
                                }
                            },
                            'message': {'type': 'string'},
                            'code': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
@jwt_required()
@manager_required
def activate_user(user_id):
    try:
        dict = UserServices().activate_user(user_id=user_id)

        return standardize_response(data=dict, message='User activated successfully', code=200)
    except Exception as e:
        raise e