from django.db import models
from django.db.models import Avg, F
from django.utils import timezone

from applications.rent.choices.room_type import RoomType
from applications.rent.managers.rent import SoftDeleteManager
from applications.rent.models.locations import Address
from applications.reviews.models.review import Review
from applications.users.models.user import User


class Rent(models.Model):
    title = models.CharField(max_length=90, db_index=True)
    description = models.TextField()
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rents'
    )
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    rooms_count = models.PositiveSmallIntegerField(default=0)
    room_type = models.CharField(max_length=36, choices=RoomType.choices())
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    avg_rating = models.FloatField(default=0.0)
    cn_views = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rents'
    )

    objects = SoftDeleteManager()

    def delete(self, *arg, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def set_cn_views(self):
        self.cn_views = F('cn_views') + 1
        self.save(update_fields=['cn_views'])
        self.refresh_from_db(fields=['cn_views'])

    def set_avg_rating(self):
        avg = Review.objects.filter(rent = self).aggregate(avg=Avg('rating'))['avg'] or 0.0
        self.avg_rating = round(avg, 1)
        self.save(update_fields=['avg_rating'])

    class Meta:
        db_table = "rent"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=[
                'title',
                'address',
                'is_deleted'
            ],
                name='unique_listing_title_desc_address_not_deleted')
        ]

    def __str__(self):
        return self.title
