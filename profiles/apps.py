from django.apps import AppConfig
import django.db.models.signals

class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
    def ready(self):
        import profiles.signals
