from app.scheduling.models import AppointmentDetail
from app.scheduling.models import Appointment  
from app.scheduling.models import TimeSlot
from app.exceptions import ExposedException

#reminder: NEED TO MAKE SURE THE RIGHT SERVICES ARE ADDED BY CHECKING ROUTES AND MODELS

class ScheduleService:
    #get all time slots
    def get_all_time_slots(self):
        try:
            time_slots=TimeSlot.get_all_time_slots()
            if time_slots == []:
                return ExposedException('No time slots available')
            else:
                return time_slots
        except Exception as e:
            raise e

    #get all avialable time slots
    def get_avialable_time_slots(self):
        try:
            avialable_time_slots = TimeSlot.get_available_time_slots()
            if avialable_time_slots == []:
                return ExposedException('No avialable time slots')
            else:
                return avialable_time_slots
        except Exception as e:
            raise e
    
    #get all appointments
    def get_all_appointments(self):
        try:
            appointments=Appointment.get_all_appointments()
            if appointments == []:
                return ExposedException('No appointments available')
            else:
                return appointments
        except Exception as e:
            raise e
        
    #create appointment
    def create_appointment(self, time_slot_id, customer_id, user_id, appointment_type, status):
        try:
            return Appointment.create_appointment(time_slot_id, customer_id, user_id, appointment_type, status)
        except Exception as e:
            raise e

    #get all appointments by customer id
    def get_all_appointments_by_customer_id(self, customer_id):
        try:
            appointments_by_customer_id=Appointment.get_all_appointments_by_customer_id(customer_id)
            if appointments_by_customer_id == []:
                return ExposedException('No appointments available')
        except Exception as e:
            raise e
    
    #get all appointments by appointment type
    def get_all_appointments_by_appointment_type(self, appointment_type):
        try:
            appointments_by_appointment_type=Appointment.get_all_appointments_by_appointment_type(appointment_type)
            if appointments_by_appointment_type == []:
                return ExposedException('No appointments available')
        except Exception as e:
            raise e
        
    #get appointment by customer id and appointment type
    def get_appointment_by_customer_id_and_appointment_type(self, customer_id, appointment_type):
        try:
            appointment_by_customer_id_and_appointment_type=Appointment.get_appointment_by_customer_id_and_appointment_type(customer_id, appointment_type)
            if appointment_by_customer_id_and_appointment_type == []:
                return ExposedException('No appointments available')
        except Exception as e:
            raise e

    #get appointment by user id and appointment type
    def get_appointment_by_user_id_and_appointment_type(self, user_id, appointment_type):
        try:
            appointment_by_user_id_and_appointment_type=Appointment.get_appointment_by_user_id_and_appointment_type(user_id, appointment_type)
            if appointment_by_user_id_and_appointment_type == []:
                return ExposedException('No appointments available')
        except Exception as e:
            raise e
    
    #get appointment by appointment id
    def get_appointment_by_appointment_id(self, appointment_id):
        try:
            appointment_by_appointment_id=Appointment.get_appointment_by_appointment_id(appointment_id)
            if appointment_by_appointment_id == []:
                return ExposedException('No appointments available')
        except Exception as e:
            raise e
    
    #get all appointments details
    def get_all_appointment_details(self):
        try:
            appointments_details=AppointmentDetail.get_all_appointment_details()
            if appointments_details == []:
                return ExposedException('No appointments details available')
        except Exception as e:
            raise e

    #cancel appointment(MIGHT NOT NEEED THIS)
    def cancel_appointment(self, appointment_id):
        try:
            return Appointment.cancel_appointment(appointment_id)
        except Exception as e:
            raise e
    
        
    