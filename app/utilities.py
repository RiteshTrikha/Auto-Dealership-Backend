from flask import jsonify

class Utilities:
    @staticmethod
    def standardize_response(status='success', data=None, message=None, code = 200):
        return jsonify({
            'status': status,
            'data': data,
            'message': message
        }), code