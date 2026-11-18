from api.booking_client import BookingClient
from conftest import BOOKING_PAYLOAD


def test_create_booking(client):
    response = client.create_booking(BOOKING_PAYLOAD)

    assert response.status_code == 200

    body = response.json()
    booking_id = body["bookingid"]

    try:
        assert booking_id > 0
        assert body["booking"] == BOOKING_PAYLOAD
    finally:
        client.delete_booking(booking_id)


def test_partial_update_booking(client, created_booking):
    new_data = {
        "firstname": "Anna",
        "lastname": "Petrova"
    }

    response = client.update_booking(
        created_booking, new_data
    )

    assert response.status_code == 200

    body = response.json()

    assert body["firstname"] == "Anna"
    assert body["lastname"] == "Petrova"
    assert body["totalprice"] == BOOKING_PAYLOAD["totalprice"]
    assert body["depositpaid"] == BOOKING_PAYLOAD["depositpaid"]
    assert body["bookingdates"] == BOOKING_PAYLOAD["bookingdates"]
    assert body["additionalneeds"] == BOOKING_PAYLOAD["additionalneeds"]


def test_delete_booking(client):
    response = client.create_booking(BOOKING_PAYLOAD)

    assert response.status_code == 200

    booking_id = response.json()["bookingid"]

    delete_response = client.delete_booking(booking_id)

    assert delete_response.status_code == 201

    get_response = client.get_booking(booking_id)

    assert get_response.status_code == 404


def test_update_without_token(created_booking):
    no_auth_client = BookingClient()

    try:
        response = no_auth_client.update_booking(
            created_booking,
            {"firstname": "Hacker"}
        )

        assert response.status_code == 403
    finally:
        no_auth_client.close()