class Utilities:

    def standardize_response(self, status='success', message='', data=None, code=200):
        return {
            "status": status,
            "message": message,
            "data": data
        }, code