from .models import Customer
from exceptions import ExposedException

class CustomerServices:

    def create(self, first_name, last_name, email, password, birth_date, drivers_license):
        try:
            customer_id = Customer.create(first_name, last_name, email, password, birth_date, drivers_license)
            if customer_id is None:
                return ExposedException('Error creating customer', 400)
            return customer_id
        except Exception as e:
            raise e
        