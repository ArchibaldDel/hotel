from rest_framework import serializers
from .models import Room, Booking   # 👈 добавили Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price_per_night", "created_at"]
        read_only_fields = ["id", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room", "date_start", "date_end", "created_at"]
        read_only_fields = ["id", "created_at"]
