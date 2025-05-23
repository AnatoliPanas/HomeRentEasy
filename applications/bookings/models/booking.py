from django.utils import timezone
from django.db import models

from applications.bookings.choices.waiting_status import WaitingStatus
from applications.rent.models import Rent
from applications.users.models import User


class Booking(models.Model):
    lessee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'LESSEE'}
    )
    rent = models.ForeignKey(
        Rent,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=WaitingStatus.choices(),
        default=WaitingStatus.PENDING.name
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='booking_valid_date_range'
            ),
            models.UniqueConstraint(
                fields=['lessee', 'rent', 'start_date', 'end_date'],
                name='unique_booking_per_user_rent_period'
            )
        ]

    def can_cancel(self):
        return timezone.now().date() < self.start_date

    def __str__(self):
        return f'{self.lessee} - {self.rent}'
