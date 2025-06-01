from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string

from applications.reviews.models.review import Review


@receiver([post_save, post_delete], sender=Review)
def update_rating(sender, instance, **kwargs):
    instance.rent.set_avg_rating()

@receiver(post_save, sender=Review)
def notify_new_review(sender, instance, created, **kwargs):
    if created:
        subject = "Новый отзыв на ваше объявление"
        sender = "HomeRentEasy@net.net"
        recipient = instance.rent.owner.email

        context = {
            "review": instance,
            "rent": instance.rent,
        }

        text_content = render_to_string(
            template_name='new_review.txt',
            context=context
        )

        html_content = render_to_string(
            template_name='new_review.html',
            context=context
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=sender,
            to=[recipient],
            headers={'List-Unsubscribe': '<mailto:unsub@example.com>'}
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()