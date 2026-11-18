import pytest
from api.booking_client import BookingClient


BOOKING_PAYLOAD = {
    "firstname": "Polina",
    "lastname": "Bobko",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-12-01",
        "checkout": "2026-12-10"
    },
    "additionalneeds": "Breakfast"
}


@pytest.fixture
def client():
    api = BookingClient()
    try:
        api.auth()
        yield api
    finally:
        api.close()


@pytest.fixture
def created_booking(client):
    response = client.create_booking(BOOKING_PAYLOAD)

    assert response.status_code == 200, response.text

    booking_id = response.json()["bookingid"]

    yield booking_id

    client.delete_booking(booking_id)