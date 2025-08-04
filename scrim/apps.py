from django.apps import AppConfig


class ScrimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrim'

# load signals.py 
    def ready(self):
        import scrim.signals

