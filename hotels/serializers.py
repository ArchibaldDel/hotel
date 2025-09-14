from rest_framework import serializers
from django.db.models import Q
from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price_per_night", "created_at"]
        read_only_fields = ["id", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(write_only=True, required=False)
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        required=False
    )

    class Meta:
        model = Booking
        fields = ["id", "room", "room_id", "date_start", "date_end", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        room_id = attrs.pop("room_id", None)
        if room_id is not None:
            try:
                attrs["room"] = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                raise serializers.ValidationError({"room_id": "Room does not exist."})

        room = attrs.get("room")
        date_start = attrs.get("date_start")
        date_end = attrs.get("date_end")

        if date_start and date_end and date_end < date_start:
            raise serializers.ValidationError({"date_end": "must be >= date_start"})

        if self.context.get("check_overlap") and room and date_start and date_end:
            overlap = Booking.objects.filter(room=room).filter(
                Q(date_start__lte=date_end) & Q(date_end__gte=date_start)
            ).exists()
            if overlap:
                raise serializers.ValidationError(
                    "Room is not available for the selected dates."
                )

        return attrs

    def create(self, validated_data):
        """Переопределяем, чтобы гарантированно работало с room_id"""
        return Booking.objects.create(**validated_data)
