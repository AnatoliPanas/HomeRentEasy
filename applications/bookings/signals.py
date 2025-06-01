from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from applications.bookings.models import Booking
from applications.bookings.choices.waiting_status import WaitingStatus


@receiver(post_save, sender=Booking)
def send_booking_status_changed(sender, instance, created, **kwargs):
    status_subjects = {
        WaitingStatus.PENDING.name: "Новое бронирование создано",
        WaitingStatus.CONFIRMED.name: "Бронирование подтверждено",
        WaitingStatus.DECLINED.name: "Бронирование отклонено",
        WaitingStatus.CANCELLED.name: "Бронирование отменено",
    }

    subject = status_subjects.get(instance.status, "Статус бронирования изменен")
    sender = "HomeRentEasy@net.net"

    if created:
        recipient = instance.rent.owner.email
        recipient_name = instance.rent.owner.first_name
        text_status = "Статус бронирования на Ваше объявление изменился на:"
    else:
        recipient = instance.lessee.email
        recipient_name = instance.lessee.first_name
        text_status = "Статус Вашего бронирования изменился на:"


    context = {
        "booking": instance,
        "recipient_name": recipient_name,
        "text_status": text_status,
    }

    text_content = render_to_string(
        template_name='booking_status_changed.txt',
        context=context
    )

    html_content = render_to_string(
        template_name='booking_status_changed.html',
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
