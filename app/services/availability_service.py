from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from app.database.db import DB
from app.models.doctor import DoctorAvailability
from app.models.requests.doctor_appointment_request import DoctorAppointmentRequest
from app.models.requests.doctor_availability_request import DoctorAvailabilityRequest
class AvailabilityService(ABC):
    # Abstract class defining the interface for managing doctor availability.

    @abstractmethod
    def add_doctor_availability(self, availability: DoctorAvailabilityRequest) -> DoctorAvailability:
        ...
    
    @abstractmethod
    def book_appointment(self, appointment: DoctorAppointmentRequest) -> DoctorAvailability:
        ...
    
    @abstractmethod
    def get_available_slots(self, doctor_id: int) -> List[DoctorAvailability]:
        ...

    @abstractmethod
    def get_booked_appointments(self, doctor_id: int) -> List[DoctorAvailability]:
        ...
    
    @abstractmethod
    def cancel_appointment(self, appointment_id: int) -> int:
        ...

class InDatabaseAvailabilityService(AvailabilityService):

    def __init__(self, db: DB):
        self.db = db
    
    def add_doctor_availability(self, availability: DoctorAvailabilityRequest) -> DoctorAvailability:
        if not self.doctor_exists(availability.doctor_id):
            # if doctor does not exist
            return { "message":f'Doctor with given Id:{availability.doctor_id} does not exist'}
        
        existing_availability = self.db.execute(
        'SELECT * FROM doctor_availability WHERE doctor_id = ? AND day_of_week = ? AND start_time = ? AND end_time = ?',
        [availability.doctor_id, availability.day_of_week, availability.start_time, availability.end_time]
        )
        
        if existing_availability:
        # for already existing availability
            return {"message":"Availability already present in the database"}

        self.db.execute(
            'INSERT INTO doctor_availability (doctor_id, day_of_week, location_id, start_time, end_time, is_available) '
            'VALUES (?, ?, ?, ?, ?,?)',
            [availability.doctor_id, availability.day_of_week, availability.location_id, availability.start_time,
            availability.end_time, 1]
        )

        id = self.db.last_row_id

        assert id
        return DoctorAvailability(
            id=id,
            doctor_id=availability.doctor_id,
            day_of_week=availability.day_of_week,
            location_id=availability.location_id,
            start_time=availability.start_time,
            end_time=availability.end_time
        )
    
    
    def get_available_slots(self, doctor_id: int) -> List[DoctorAvailability]:
        # available slots for a particular doctor
        if not self.doctor_exists(doctor_id):
            return { "message":f'Doctor with given Id:{doctor_id} does not exist'}
        
        dict_result =self.doctor_slot(doctor_id,1)
        
        return [DoctorAvailability(**res) for res in dict_result]
    

    def get_booked_appointments(self, doctor_id: int) -> List[DoctorAvailability]:
        # booked slots for a particular doctor
        if not self.doctor_exists(doctor_id):
            return { "message":f'Doctor with given Id:{doctor_id} does not exist'}
        
        dict_result =self.doctor_slot(doctor_id,0)
        
        return [DoctorAvailability(**res) for res in dict_result]
    

    def book_appointment(self, appointment: DoctorAppointmentRequest) -> DoctorAvailability:
        # Book a new appointment for a doctor if not already present.
        start_time=appointment.time.split('-')[0]
        end_time=appointment.time.split('-')[1]

        if not self.doctor_exists(appointment.doctor_id):
            return { "message":f'Doctor with given Id:{appointment.doctor_id} does not exist'}
        
        dict_result = self.db.execute(
            'SELECT id, is_available FROM doctor_availability WHERE doctor_id = ? '
            'AND day_of_week = ? AND start_time = ? AND end_time = ?',
            [appointment.doctor_id,  appointment.day_of_week,
            start_time, end_time]
            )
        
        if  not dict_result[0]['is_available']:
            return {"message":"An appointment already exist"}
        
        # Update the database with the new value
        self.db.execute(
            'UPDATE doctor_availability SET is_available = ? WHERE id = ?',
            [0, dict_result[0]['id']]
        ) 

        return DoctorAvailability(
            id=dict_result[0]['id'],
            doctor_id=appointment.doctor_id,
            location_id=appointment.location_id,
            day_of_week=appointment.day_of_week,
            start_time=start_time,
            end_time=end_time
        )

    def cancel_appointment(self, availability_id: int):
    # Fetch the current value of `is_available`
    
        current_value = self.db.execute(
            'SELECT is_available FROM doctor_availability WHERE id = ?',
            [availability_id]
        )
        # if 1 => it is not booked
        if current_value is None:
            return {"message":f'No such appointment exist with {availability_id}'}

        
        # Update the database with the new value
        self.db.execute(
            'UPDATE doctor_availability SET is_available = ? WHERE id = ?',
            [1, availability_id]
        )
        return availability_id 


    def doctor_exists(self, doctor_id: int) -> bool:
        
        result = self.db.execute(
            "SELECT 1 FROM doctors WHERE id = ?",
            (doctor_id,)
        )
        return result
    
    def doctor_slot(self, doctor_id: int, is_available:int ) -> bool:
        
        dict_result = self.db.execute(
            'SELECT id, doctor_id, day_of_week, location_id, start_time, end_time '
            'FROM doctor_availability '
            'WHERE doctor_id = ? AND is_available = ?',
            [doctor_id,is_available]
        )
        return dict_result
    