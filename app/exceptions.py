class ExposedException(Exception):
    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return {
            'message': self.message,
        }
    