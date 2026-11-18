import requests


class BookingClient:
    BASE_URL = "https://restful-booker.herokuapp.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.token = None

    def auth(self):
        response = self.session.post(
            f"{self.BASE_URL}/auth",
            json={
                "username": "admin",
                "password": "password123"
            },
            timeout=15
        )
        response.raise_for_status()
        self.token = response.json()["token"]

    def create_booking(self, data):
        return self.session.post(
            f"{self.BASE_URL}/booking",
            json=data,
            timeout=15
        )

    def get_booking(self, booking_id):
        return self.session.get(
            f"{self.BASE_URL}/booking/{booking_id}",
            timeout=15
        )

    def update_booking(self, booking_id, data):
        return self.session.patch(
            f"{self.BASE_URL}/booking/{booking_id}",
            json=data,
            headers={"Cookie": f"token={self.token}"},
            timeout=15
        )

    def delete_booking(self, booking_id):
        return self.session.delete(
            f"{self.BASE_URL}/booking/{booking_id}",
            headers={"Cookie": f"token={self.token}"},
            timeout=15
        )

    def close(self):
        self.session.close()