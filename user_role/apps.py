# user_role/apps.py
from django.apps import AppConfig

class UserRoleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_role'

    def ready(self):
        # Import signals to connect `post_migrate` handler
        import user_role.signals
