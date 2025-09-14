import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from hotels.models import Room, Booking

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

def test_delete_room_cascade(api_client):
    room = Room.objects.create(description="To delete", price_per_night=999)
    Booking.objects.create(room=room, date_start="2025-09-01", date_end="2025-09-05")

    url = reverse("room-delete", kwargs={"pk": room.id})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Room.objects.count() == 0
    assert Booking.objects.count() == 0

def test_delete_booking(api_client):
    room = Room.objects.create(description="R", price_per_night=777)
    booking = Booking.objects.create(room=room, date_start="2025-09-10", date_end="2025-09-12")

    url = reverse("booking-delete", kwargs={"pk": booking.id})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Booking.objects.count() == 0
