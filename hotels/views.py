from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({
            "service": "hotel-booking-api",
            "status": "healthy"
        })


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price_per_night", "created_at"]
    ordering = ["created_at"]

class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"   # <-- добавь это

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Список броней по room_id
class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get("room_id")
        if room_id:
            return Booking.objects.filter(room_id=room_id).order_by("date_start")
        return Booking.objects.none()


class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = "pk"   # <-- добавь это
