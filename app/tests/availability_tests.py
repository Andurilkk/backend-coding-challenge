from fastapi.testclient import TestClient
import pytest

from app.settings import Settings


@pytest.fixture(autouse=True, params=[True, False])
def mode(request) -> None:
    Settings.in_database = request.param


# Test for adding doctor availability
def test_add_availability(client: TestClient):
    response = client.post(
        "/availabilities",
        json={
            "doctor_id": 1,
            "day_of_week": "Monday",
            "location_id": 0,
            "start_time": "09:00",
            "end_time": "17:00",
            "is_available":1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["doctor_id"] == 0
    assert data["day_of_week"] == "Monday"
    assert data["location_id"] == 0
    assert data["start_time"] == "09:00"
    assert data["end_time"] == "17:00"
    assert data["is_available"] == 1

# Test for getting availabilities for a specific doctor
def test_get_availabilities_for_doctor(client: TestClient):
    response = client.get("/doctors/0/availabilities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["doctor_id"] == 0
    assert data[0]["day_of_week"] == "Monday"
    assert data[0]["is_available"] == 1

# Test for getting availabilities for a specific doctor
def test_get_appointments_for_doctor(client: TestClient):
    response = client.get("/doctors/0/booked_appointments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["doctor_id"] == 0
    assert data[0]["day_of_week"] == "Monday"
    assert data[0]["is_available"] == 1


# Test for booking an appointment
def test_book_appointment(client: TestClient):
    response = client.put(
        "/availabilities/1/appointment",
        json={
            "doctor_id": 0,
            "location_id": 0,
            "day_of_week": "Monday",
            "time": "09:00-10:00"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["doctor_id"] == 0
    assert data["location_id"] == 0
    assert data["day_of_week"] == "Monday"
    assert data["start_time"] == "09:00"
    assert data["end_time"] == "10:00"

# Test for booking an appointment with an invalid doctor ID
def test_book_appointment_invalid_doctor(client: TestClient):
    response = client.put(
        "/availabilities/1/appointment",
        json={
            "doctor_id": 999,
            "location_id": 0,
            "day_of_week": "Monday",
            "time": "09:00-10:00"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Doctor with given Id:999 does not exist" in data["message"]

# Test for canceling an appointment
def test_cancel_appointment(client: TestClient):
    response = client.put("/availabilities/0/cancelAppointment")
    assert response.status_code == 200
    data = response.json()
    assert "message" not in data
    assert data == 0

# Test for canceling an appointment with an invalid ID
def test_cancel_invalid_appointment(client: TestClient):
    response = client.put("/availabilities/999/cancelAppointment")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "No such appointment exist with 999" in data["message"]