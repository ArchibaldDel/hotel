from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({"service": "hotel-booking-api", "status": "healthy"})


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price_per_night", "created_at"]
    ordering = ["id"]


class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get("room_id")
        qs = Booking.objects.all()
        if room_id:
            qs = qs.filter(room_id=room_id)
        return qs.order_by("date_start")


class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = "pk"


class BookingCreateLegacyView(APIView):
    """
    POST /bookings/create
    form-data: room_id=24, date_start=YYYY-MM-DD, date_end=YYYY-MM-DD
    response: {"booking_id": <int>}
    """

    def post(self, request):
        serializer = BookingSerializer(
            data=request.data,
            context={"check_overlap": False},
        )
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)


class BookingListLegacyView(APIView):
    """
    GET /bookings/list?room_id=24
    response: [{"booking_id": ..., "date_start": "...","date_end": "..."}]
    """

    def get(self, request):
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response({"error": "room_id is required"}, status=400)
        bookings = Booking.objects.filter(room_id=room_id).order_by("date_start")
        data = [
            {
                "booking_id": b.id,
                "date_start": str(b.date_start),
                "date_end": str(b.date_end),
            }
            for b in bookings
        ]
        return Response(data, status=200)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["check_overlap"] = True
        return context
