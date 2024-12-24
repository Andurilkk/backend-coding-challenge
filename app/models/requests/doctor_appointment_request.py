from pydantic import BaseModel

class DoctorAppointmentRequest(BaseModel):
    location_id: int
    doctor_id: int
    day_of_week: str
    time: str