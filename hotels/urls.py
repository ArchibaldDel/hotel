from django.urls import path
from .views import (
    HealthView,
    RoomCreateView, RoomListView, RoomDeleteView,
    BookingCreateView, BookingListView, BookingDeleteView
)

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),

    # Rooms
    path("rooms/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/list/", RoomListView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDeleteView.as_view(), name="room-delete"),

    # Bookings
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/list/", BookingListView.as_view(), name="booking-list"),
    path("bookings/<int:pk>/", BookingDeleteView.as_view(), name="booking-delete"),
]
