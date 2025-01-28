from django.apps import AppConfig


class SearchesConfig(AppConfig):
    name = 'searches'

# blog/apps.py
from django.apps import AppConfig

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'