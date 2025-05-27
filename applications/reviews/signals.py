from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from applications.reviews.models.review import Review


@receiver([post_save, post_delete], sender=Review)
def update_rating(sender, instance, **kwargs):
    instance.rent.set_avg_rating()