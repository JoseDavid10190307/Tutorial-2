from django.apps import AppConfig
from django.utils.module_loading import import_string
from django.conf import settings


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    


