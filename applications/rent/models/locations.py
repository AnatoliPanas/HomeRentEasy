from django.db import models

from applications.users.models import User


class Address(models.Model):
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=65)
    street = models.CharField(max_length=128)
    house_number = models.CharField(max_length=16, blank=True, null=True)
    apartment_number = models.CharField(max_length=16, blank=True, null=True)
    postal_code = models.CharField(max_length=19, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'address'
        constraints = [
            models.UniqueConstraint(fields=[
                'country',
                'city',
                'street',
                'apartment_number'
            ],
                name='unique_address_with_apartment')
        ]

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='addresses'
    )

    def __str__(self):
        parts = [self.city, self.street, self.house_number]
        return ', '.join(filter(None, parts))
