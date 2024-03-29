from .models import Vehical, RetailItem

class InventoryService:
    
    def get_vehicle(self, vehical_id):
        try:
            vehicle = Vehical.get_vehicle(vehical_id)
            return vehicle
        except Exception as e:
            raise e
    
    def get_all_vehicles(self):
        try:
            vehicles = Vehical.get_all_vehicles()
            return vehicles
        except Exception as e:
            raise e
        
    def get_top_5_vehicles(self):
        try:
            vehicles = Vehical.get_top_5_vehicles()
            return vehicles
        except Exception as e:
            raise e