from pydantic import BaseModel,validator
# When an entry is made for availability table for a doctor it is considered that it is an available slot
class DoctorAvailabilityRequest(BaseModel):
    doctor_id:int
    day_of_week :str
    location_id:int
    start_time :str
    end_time :str

