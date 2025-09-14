import pytest
from hotels.models import Room, Booking


@pytest.mark.django_db
def test_room_str():
    room = Room.objects.create(description="Luxury Suite", price_per_night=5000)
    assert "Luxury Suite" in str(room)


@pytest.mark.django_db
def test_booking_str():
    room = Room.objects.create(description="Test", price_per_night=1000)
    booking = Booking.objects.create(
        room=room, date_start="2025-09-20", date_end="2025-09-25"
    )
    assert f"Booking {booking.id}" in str(booking)
