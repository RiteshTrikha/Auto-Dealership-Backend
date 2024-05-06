from app.utilities import Utilities
standardize_response = Utilities.standardize_response


class ExposedException(Exception):
    def __init__(self, message, code=400):
        self.status = 'error'
        self.message = message
        self.code = code

    def to_dict(self):
        return {
            'status': self.status,
            'message': self.message,
            'code': self.code
        }
    
class ExpDatabaseException(ExposedException):
    def __init__(self, message='database error occurred', code=500):
        super().__init__(message, code)