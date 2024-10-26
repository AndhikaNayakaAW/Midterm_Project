from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

# Function to check if user is in 'Admin' group
def admin_check(user):
    return user.groups.filter(name='Admin').exists()

def create_user_groups():
    # Define the groups you want to create
    groups = ['User', 'Admin']

    # Create groups if they don't already exist
    for group in groups:
        if not Group.objects.filter(name=group).exists():
            Group.objects.create(name=group)
