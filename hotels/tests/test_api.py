import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from hotels.models import Room, Booking


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_room(api_client):
    url = reverse("room-create")
    response = api_client.post(url, {
        "description": "Test room",
        "price_per_night": "1234.56"
    }, format="json")
    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["description"] == "Test room"


@pytest.mark.django_db
def test_list_rooms(api_client):
    Room.objects.create(description="R1", price_per_night=100)
    Room.objects.create(description="R2", price_per_night=200)

    url = reverse("room-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 2


@pytest.mark.django_db
def test_list_rooms_ordering(api_client):
    Room.objects.create(description="Cheap", price_per_night=100)
    Room.objects.create(description="Expensive", price_per_night=1000)

    url = reverse("room-list") + "?ordering=price_per_night"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]["description"] == "Cheap"

    url = reverse("room-list") + "?ordering=-price_per_night"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]["description"] == "Expensive"


@pytest.mark.django_db
def test_delete_room_cascade(api_client):
    room = Room.objects.create(description="Cascade delete", price_per_night=500)
    Booking.objects.create(room=room, date_start="2025-09-01", date_end="2025-09-05")

    url = reverse("room-delete", kwargs={"pk": room.id})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Room.objects.filter(id=room.id).count() == 0
    assert Booking.objects.filter(room=room).count() == 0


@pytest.mark.django_db
def test_create_booking(api_client):
    room = Room.objects.create(description="With booking", price_per_night=777)

    url = reverse("booking-create")
    response = api_client.post(url, {
        "room": room.id,
        "date_start": "2025-09-10",
        "date_end": "2025-09-15"
    }, format="json")

    assert response.status_code == 201
    assert response.data["room"] == room.id


@pytest.mark.django_db
def test_create_booking_with_room_id(api_client):
    room = Room.objects.create(description="Room with room_id", price_per_night=500)

    url = reverse("booking-create")
    response = api_client.post(url, {
        "room_id": room.id,
        "date_start": "2025-09-20",
        "date_end": "2025-09-22"
    }, format="json")

    assert response.status_code == 201
    assert response.data["room"] == room.id


@pytest.mark.django_db
def test_create_booking_with_nonexistent_room(api_client):
    url = reverse("booking-create")
    response = api_client.post(url, {
        "room_id": 9999,
        "date_start": "2025-09-20",
        "date_end": "2025-09-22"
    }, format="json")

    assert response.status_code == 400
    assert "room_id" in response.data or "room" in response.data


@pytest.mark.django_db
def test_list_bookings(api_client):
    room = Room.objects.create(description="Room for bookings", price_per_night=300)
    Booking.objects.create(room=room, date_start="2025-09-01", date_end="2025-09-05")
    Booking.objects.create(room=room, date_start="2025-09-10", date_end="2025-09-12")

    url = reverse("booking-list") + f"?room_id={room.id}"
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["date_start"] < response.data[1]["date_start"]


@pytest.mark.django_db
def test_delete_booking(api_client):
    room = Room.objects.create(description="Delete booking", price_per_night=400)
    booking = Booking.objects.create(room=room, date_start="2025-09-01", date_end="2025-09-05")

    url = reverse("booking-delete", kwargs={"pk": booking.id})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Booking.objects.filter(id=booking.id).count() == 0


@pytest.mark.django_db
def test_invalid_booking_dates_format(api_client):
    room = Room.objects.create(description="Invalid booking", price_per_night=900)

    url = reverse("booking-create")
    response = api_client.post(url, {
        "room": room.id,
        "date_start": "invalid-date",
        "date_end": "2025-09-15"
    }, format="json")

    assert response.status_code == 400
    assert "date_start" in response.data


@pytest.mark.django_db
def test_invalid_booking_date_range(api_client):
    room = Room.objects.create(description="Range booking", price_per_night=900)

    url = reverse("booking-create")
    response = api_client.post(url, {
        "room": room.id,
        "date_start": "2025-09-15",
        "date_end": "2025-09-10"
    }, format="json")

    assert response.status_code == 400
    assert "date_end" in response.data


@pytest.mark.django_db
def test_booking_overlap(api_client):
    room = Room.objects.create(description="Overlap room", price_per_night=800)
    Booking.objects.create(room=room, date_start="2025-09-10", date_end="2025-09-15")

    url = reverse("booking-create")
    response = api_client.post(url, {
        "room": room.id,
        "date_start": "2025-09-12",
        "date_end": "2025-09-20"
    }, format="json")

    assert response.status_code == 400
    assert "Room is not available" in str(response.data)
