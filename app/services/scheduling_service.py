from app.scheduling.models import AppointmentDetail
from app.scheduling.models import Appointment  
from app.scheduling.models import TimeSlot

class ScheduleService:
    
    def get_avialable_time_slots(self):
        try:
            return TimeSlot.get_available_time_slots()
        except Exception as e:
            raise e
        
    def get_all_appointments(self):
        try:
            return Appointment.get_all_appointments()
        except Exception as e:
            raise e
    pass

    def create_appointment(self, time_slot_id, customer_id, user_id, appointment_type, status):
        try:
            return Appointment.create_appointment(time_slot_id, customer_id, user_id, appointment_type, status)
        except Exception as e:
            raise e

    def get_all_appointments_by_customer_id_and_appointment_type(self, customer_id, appointment_type):
        try:
            return Appointment.get_appointments_by_customer_id_and_appointment_type(customer_id, appointment_type)
        except Exception as e:
            raise e
    
    def get_all_appointments_by_appointment_type(self, appointment_type):
        try:
            return Appointment.get_appointments_by_appointment_type(appointment_type)
        except Exception as e:
            raise e

    def get_all_appointment_details(self):
        try:
            return AppointmentDetail.get_all_appointment_details()
        except Exception as e:
            raise e
    
    #Cancel an appointment
    