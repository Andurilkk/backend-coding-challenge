from typing import Optional
from app.models.requests.doctor_appointment_request import DoctorAppointmentRequest
from app.models.requests.doctor_availability_request import DoctorAvailabilityRequest
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from app.database.db import DB
from app.models.error import NotFoundException
from app.models.requests.add_doctor_request import AddDoctorRequest, AddAvailabilityRequest
from app.services.doctor_service import DoctorService, InDatabaseDoctorService, InMemoryDoctorService
from app.services.availability_service import InDatabaseAvailabilityService
from app.settings import Settings


def create_app() -> FastAPI:
    doctor_service: DoctorService
    db: Optional[DB] = None
    if Settings.in_database:
        db = DB()
        db.init_if_needed()
        doctor_service = InDatabaseDoctorService(db=db)
        availability_service = InDatabaseAvailabilityService(db=db)
    else:
        doctor_service = InMemoryDoctorService()
        doctor_service.seed()

    app = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True})

    @app.get('/doctors')
    def list_doctors():
        return doctor_service.list_doctors()

    @app.get('/doctors/{id}')
    async def get_doctor(id: int):
        return doctor_service.get_doctor(id)

    @app.post('/doctors')
    def add_doctor(request: AddDoctorRequest):
        id = doctor_service.add_doctor(
            first_name=request.first_name,
            last_name=request.last_name
        )

        return {
            'id': id
        }

    @app.get('/doctors/{doctor_id}/locations')
    def get_doctor_locations(doctor_id: int):
        return doctor_service.list_doctor_locations(doctor_id=doctor_id)

    # Add new endpoints here! #

# for adding availability of a doctor
    @app.post('/availabilities')
    def add_availability(request: DoctorAvailabilityRequest):
        return  availability_service.add_doctor_availability(
            availability=request
        )
        
# check available slot for a doctor
    @app.get('/doctors/{doctor_id}/availabilities')
    def get_availabilities_for_doctor(doctor_id: int):
        return availability_service.get_available_slots(doctor_id=doctor_id)

# book an appointment with doctor
    @app.put('/availabilities/{availability_id}/appointment')
    def book_appointment(request:DoctorAppointmentRequest):
        return availability_service.book_appointment(
            appointment=request
        )

# booked appointment for a doctor
    @app.get('/doctors/{doctor_id}/booked_appointments')
    def get_booked_appointments(doctor_id: int):
        return availability_service.get_booked_appointments(doctor_id=doctor_id)
    
# cancel appointment
    @app.put('/availabilities/{availability_id}/cancelAppointment')
    def cancel_appointment(availability_id: int):
        return availability_service.cancel_appointment(
            availability_id=availability_id
        )

    
    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return Response(status_code=404)

    @app.on_event('shutdown')
    def shutdown():
        if db:
            db.close_db()

    @app.get('/', include_in_schema=False)
    def root():
        return RedirectResponse('/docs')

    return app


app = create_app()
