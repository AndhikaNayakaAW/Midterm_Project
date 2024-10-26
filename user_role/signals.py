# user_role/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .views import create_user_groups  # or wherever create_user_groups is defined

@receiver(post_migrate)
def create_groups_after_migrate(sender, **kwargs):
    create_user_groups()
