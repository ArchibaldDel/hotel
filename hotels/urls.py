from django.urls import path
from .views import (
    HealthView,
    RoomCreateView,
    RoomListView,
    RoomDeleteView,
    BookingCreateView,
    BookingListView,
    BookingDeleteView,
    BookingCreateLegacyView,
    BookingListLegacyView,
)

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),
    # Твои основные REST-ручки (оставляем как есть)
    path("rooms/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/list/", RoomListView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDeleteView.as_view(), name="room-delete"),
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/list/", BookingListView.as_view(), name="booking-list"),
    path("bookings/<int:pk>/", BookingDeleteView.as_view(), name="booking-delete"),
    # Legacy-ручки под точное ТЗ (без конечного слэша и с нужным форматом ответа)
    path(
        "bookings/create",
        BookingCreateLegacyView.as_view(),
        name="booking-create-legacy",
    ),
    path("bookings/list", BookingListLegacyView.as_view(), name="booking-list-legacy"),
]
