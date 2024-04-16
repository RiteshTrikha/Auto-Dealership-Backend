from flask import current_app, g
from .models import Appointment, TimeSlot, Service, Service_Ticket, Service_Ticket_Service
from app.inventory.models import Vehical
from app.customer.models import Customer, CustomerVehical
from app.exceptions import ExposedException, ExpDatabaseException
from app import db

#Logic for scheduling appointments 
class ScheduleService:


############## SCHEDULE APPOINTMENTS ####################
    
    #pick a time slot for a test drive and create a test drive appointment with the status pending(3) and appointment type test drive(2) and update time slot is_available to unavailable(0)
    def schedule_test_drive(self, customer_id, time_slot_id):
        try:
            #create test drive appointment
            appointment = Appointment.create_appointment(customer_id, time_slot_id, Appointment.appointmentType.TEST_DRIVE.value, Appointment.Status.PENDING.value)
            
            #update time slot
            time_slot = TimeSlot.get_time_slot_by_time_slot_id(time_slot_id)
            time_slot.is_available = 0
            db.session.commit()
            
            return appointment.appointment_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e


    #pick a time slot for a service appointment and create a service appointment with the status pending(3) and appointment type service(1) and update time slot is_available to unavailable(0) and create service ticket with the services selected
    def schedule_service(self, user_id, customer_id, time_slot_id, customer_vehicle_id, customer_notes, technician_notes, services):
        try:
            #create service appointment
            appointment = Appointment.create_appointment(customer_id, time_slot_id, Appointment.appointmentType.SERVICE.value, Appointment.Status.PENDING.value)
            
            #update time slot
            time_slot = TimeSlot.get_time_slot_by_time_slot_id(time_slot_id)
            time_slot.is_available = 0
            
            #create service ticket
            service_ticket = Service_Ticket.create_service_ticket(customer_id=customer_id, user_id=user_id, customer_vehicle_id=customer_vehicle_id, time_slot_id=time_slot_id, customer_notes=customer_notes, technician_notes=technician_notes, status=Service_Ticket.Status.OPEN.value)

            #get service by service_id
            for service in services:
                service = Service.get_service_by_service_id(service['service_id'])
                if service is None:
                    raise ExposedException("Service not found", code = 404)
                #create service ticket service
                Service_Ticket_Service.create_service_ticket_service(service_ticket_id=service_ticket.service_ticket_id, service_id=service.service_id)

            db.session.commit()
            return appointment.appointment_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
############## Cancel APPOINTMENTS ####################

    #cancel a appointment and update time slot is_available to available(1)
    def cancel_appointment(self, appointment_id):
        try:
            #get appointment
            appointment = Appointment.get_appointment_by_appointment_id(appointment_id)
            if appointment is None:
                raise ExposedException("Appointment not found", code = 404)
            #cancel appointment
            Appointment.update_appointment_status(appointment_id, Appointment.Status.CANCELLED.value)
            
            #update time slot
            time_slot = TimeSlot.get_time_slot_by_time_slot_id(appointment.time_slot_id)
            time_slot.is_available = 1

            #get service ticket by time slot id only if appointment type is service
            if appointment.appointment_type == Appointment.appointmentType.SERVICE.value:
                service_ticket = Service_Ticket.get_service_ticket_by_time_slot_id(appointment.time_slot_id)
                if service_ticket is None:
                    raise ExposedException("Service ticket not found", code = 404)
                #cancel service ticket
                Service_Ticket.update_service_ticket_status(service_ticket.service_ticket_id, Service_Ticket.Status.CANCELLED.value)           

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
 


############## GET APPOINTMENTS FOR CUSTOMERS#################### 

    #get all appointments for a customer
    def get_appointments_by_customer_id(self, customer_id):
        try:
            appointments = Appointment.get_all_appointments_by_customer_id(customer_id)
            if appointments is None:
                raise ExposedException("No appointments found", code = 404)
            return {
                'appointments': [{
                    'appointment_id': appointment.appointment_id,
                    'customer_id': appointment.customer_id,
                    'time_slot_id': appointment.time_slot_id,
                    'appointment_type': Appointment.appointmentType(appointment.appointment_type).name,
                    'status': Appointment.Status(appointment.status).name,
                } for appointment in appointments]
            } 
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    #get all test drive appointments for a customer
    def get_test_drive_appointments(self, customer_id):
        try:
            appointments = Appointment.get_test_drive_appointments(customer_id)
            if appointments is None:
                raise ExposedException("No test drive appointments found", code = 404)
            return {
                'appointments': [{
                    'appointment_id': appointment.appointment_id,
                    'customer_id': appointment.customer_id,
                    'time_slot_id': appointment.time_slot_id,
                    'appointment_type': Appointment.appointmentType(appointment.appointment_type).name,
                    'status': Appointment.Status(appointment.status).name,
                } for appointment in appointments]
            } 
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    #get all service appointments for a customer
    def get_service_appointments_by_cutomer_id(self, customer_id):
        try:
            appointments = Appointment.get_service_appointments_by_customer_id(customer_id)
            if appointments is None:
                raise ExposedException("No service appointments found", code = 404)
            return {
                'appointments': [{
                    'appointment_id': appointment.appointment_id,
                    'customer_id': appointment.customer_id,
                    'time_slot_id': appointment.time_slot_id,
                    'appointment_type': Appointment.appointmentType(appointment.appointment_type).name,
                    'status': Appointment.Status(appointment.status).name,
                } for appointment in appointments]
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
        
############## GET APPOINTMENTS FOR USERS ####################

    #get all appointments
    def get_all_appointments(self):
        try:
            appointments = Appointment.get_all_appointments()
            if appointments is None:
                raise ExposedException("No appointments found", code = 404)
            return {
                'appointments': [{
                    'appointment_id': appointment.appointment_id,
                    'customer_id': appointment.customer_id,
                    'time_slot_id': appointment.time_slot_id,
                    'appointment_type': Appointment.appointmentType(appointment.appointment_type).name,
                    'status': Appointment.Status(appointment.status).name,
                } for appointment in appointments]
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    #get test drive appointments
    def get_test_drive_appointments(self):
        try:
            appointments = Appointment.get_test_drive_appointments()
            if appointments is None:
                raise ExposedException("No test drive appointments found", code = 404)
            return {
                'appointments': [{
                    'appointment_id': appointment.appointment_id,
                    'customer_id': appointment.customer_id,
                    'time_slot_id': appointment.time_slot_id,
                    'appointment_type': Appointment.appointmentType(appointment.appointment_type).name,
                    'status': Appointment.Status(appointment.status).name,
                } for appointment in appointments]
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e

    #get service appointments
    def get_service_appointments(self):
        try:
            appointments = Appointment.get_service_appointments()
            if appointments is None:
                raise ExposedException("No service appointments found", code = 404)
            return {
                'appointments': [{
                    'appointment_id': appointment.appointment_id,
                    'customer_id': appointment.customer_id,
                    'time_slot_id': appointment.time_slot_id,
                    'appointment_type': Appointment.appointmentType(appointment.appointment_type).name,
                    'status': Appointment.Status(appointment.status).name,
                } for appointment in appointments]
            }
        except Exception as e:
            current_app.logger.exception(e)
            raise e
    
    #get all appointments with service tickets
    def get_all_appointments_with_service_ticket(self):
        try:
            appointments = Appointment.get_service_appointments()
            if appointments is None:
                raise ExposedException("No service appointments found", code = 404)
            service_ticket = Service_Ticket.get_all_service_tickets_by_time_slot_id(appointments.time_slot_id)            
            return {
                'appointments': [{
                    'appointment_id': appointment.appointment_id,
                    'customer_id': appointment.customer_id,
                    'time_slot_id': appointment.time_slot_id,
                    'appointment_type': Appointment.appointmentType(appointment.appointment_type).name,
                    'status': Appointment.Status(appointment.status).name,
                    'service_ticket': [{
                        'service_ticket_id': service.service_ticket_id,
                        'customer_id': service.customer_id,
                        'user_id': service.user_id,
                        'customer_vehicle_id': service.customer_vehicle_id,
                        'time_slot_id': service.time_slot_id,
                        'customer_notes': service.customer_notes,
                        'technician_notes': service.technician_notes,
                        'status': Service_Ticket.Status(service.status).name,
                    } for service in service_ticket]
                } for appointment in appointments]
            }
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e

############## Assign Technician to Service Ticket ####################

    #assign technician to service ticket
    def assign_technician(self, user_id, service_ticket_id):
        try:
            #get service ticket
            service_ticket = Service_Ticket.get_service_ticket_by_service_ticket_id(service_ticket_id)
            if service_ticket is None:
                raise ExposedException("Service ticket not found", code = 404)
            #assign technician
            service_ticket.technician_id = user_id
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
############## Add Customer Notes to Service Ticket ####################

    #add customer notes to service ticket
    def add_customer_notes(self, customer_notes, service_ticket_id):
        try:
            #get service ticket
            service_ticket = Service_Ticket.get_service_ticket_by_service_ticket_id(service_ticket_id)
            if service_ticket is None:
                raise ExposedException("Service ticket not found", code = 404)
            #add customer notes
            Service_Ticket.add_customer_notes_to_service_ticket(service_ticket_id, customer_notes)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
############## Add Technician Notes to Service Ticket ####################
    
    #add technician notes to service ticket
    def add_technician_notes(self, technician_notes, service_ticket_id):
        try:
            #get service ticket
            service_ticket = Service_Ticket.get_service_ticket_by_service_ticket_id(service_ticket_id)
            if service_ticket is None:
                raise ExposedException("Service ticket not found", code = 404)
            #add technician notes
            Service_Ticket.add_technician_notes_to_service_ticket(service_ticket_id, technician_notes)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e
        
############## Update Service Ticket Status (Close Ticket) ####################

    #update service ticket status to closed
    def close_service_ticket(self, service_ticket_id):
        try:
            #get service ticket
            service_ticket = Service_Ticket.get_service_ticket_by_service_ticket_id(service_ticket_id)
            if service_ticket is None:
                raise ExposedException("Service ticket not found", code = 404)
            #close service ticket
            Service_Ticket.update_service_ticket_status(service_ticket_id, Service_Ticket.Status.CLOSED.value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            raise e