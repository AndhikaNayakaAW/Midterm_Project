# Generated by Django 5.1.1 on 2024-10-24 12:07

import uuid
from django.db import migrations, models
from django.core.management import call_command


def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "restaurants_database.json")


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Restaurants",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("island", models.CharField(max_length=100)),
                ("cuisine", models.CharField(max_length=100)),
                ("contacts", models.CharField(max_length=100)),
                ("gmaps", models.TextField()),
                ("image", models.TextField(default="")),
            ],
        ),
        migrations.RunPython(load_my_initial_data),
    ]
