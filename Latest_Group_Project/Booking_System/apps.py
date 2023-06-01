from django.apps import AppConfig
from django.contrib.auth import get_user_model

class CustomCommandsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_commands'

class BookingSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Booking_System'

    def ready(self):
        import Booking_System.signals