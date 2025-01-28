from django.apps import AppConfig


class PojaniceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pojanice'


# pojanice/apps.py
from django.apps import AppConfig

class PojaniceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pojanice'  # Ensure this matches the app's directory name