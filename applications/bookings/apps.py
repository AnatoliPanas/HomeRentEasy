from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.bookings'

    def ready(self):
        import applications.bookings.signals
