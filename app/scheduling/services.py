from app.scheduling.models import AppointmentDetail
from app.scheduling.models import Appointment  
from app.scheduling.models import TimeSlot
from app.exceptions import ExposedException

class ScheduleService:
    #get all time slots
    def get_all_time_slots(self):
        try:
            return TimeSlot.get_all_time_slots()
            if time_slots == []:
                return ExposedException('No time slots available')
        except Exception as e:
            raise e

    
    # #get all avialable time slots
    # def get_avialable_time_slots(self):
    #     try:
    #         return TimeSlot.get_available_time_slots()
    #     except Exception as e:
    #         raise e
        
    # #get all appointments
    # def get_all_appointments(self):
    #     try:
    #         return Appointment.get_all_appointments()
    #     except Exception as e:
    #         raise e
    # pass

    # #create appointment
    # def create_appointment(self, time_slot_id, customer_id, user_id, appointment_type, status):
    #     try:
    #         return Appointment.create_appointment(time_slot_id, customer_id, user_id, appointment_type, status)
    #     except Exception as e:
    #         raise e

    # #get all appointments by customer id and appointment type
    # def get_all_appointments_by_customer_id_and_appointment_type(self, customer_id, appointment_type):
    #     try:
    #         return Appointment.get_all_appointments_by_customer_id_and_appointment_type(customer_id, appointment_type)
    #     except Exception as e:
    #         raise e
    
    # #get all appointments by user id and appointment type
    # def get_all_appointments_by_appointment_type(self, appointment_type):
    #     try:
    #         return Appointment.get_all_appointments_by_appointment_type(appointment_type)
    #     except Exception as e:
    #         raise e

    # #get all appointment details
    # def get_all_appointment_details(self):
    #     try:
    #         return AppointmentDetail.get_all_appointment_details()
    #     except Exception as e:
    #         raise e
    
    # #Cancel an appointment (maybe by customer or user)
    # def cancel_appointment(self, appointment_id):
    #     try:
    #         return Appointment.cancel_appointment(appointment_id)
    #     except Exception as e:
    #         raise e
        
    