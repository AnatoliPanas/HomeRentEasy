from datetime import timedelta

from django.utils import timezone
from django.db import models

from applications.bookings.choices.waiting_status import WaitingStatus
from applications.rent.models.rent import Rent
from applications.users.models import User


class Booking(models.Model):
    lessee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'LESSEE'},
        db_index=True
    )
    rent = models.ForeignKey(
        Rent,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_index=True
    )
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    status = models.CharField(
        max_length=10,
        choices=WaitingStatus.choices(),
        default=WaitingStatus.PENDING.name,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        indexes = [
            models.Index(fields=['rent', 'start_date', 'end_date'], name='booking_date_check_idx'),
            models.Index(fields=['status', 'start_date'], name='booking_status_date_idx'),
        ]

    def can_cancel(self):
        return (self.status == WaitingStatus.CONFIRMED.name and
                timezone.now().date() < self.start_date - timedelta(days=2))

    def __str__(self):
        return f'{self.lessee} - {self.rent}'
