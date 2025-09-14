from django.db import models


class Room(models.Model):
    description = models.TextField()  # текстовое описание номера
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # цена
    created_at = models.DateTimeField(auto_now_add=True)  # когда создан

    def __str__(self):
        return f"Room {self.id}: {self.description[:20]}"

class Booking(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,  # если удалим комнату → удалятся все её брони
        related_name="bookings"
    )
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} for Room {self.room_id} ({self.date_start} - {self.date_end})"

