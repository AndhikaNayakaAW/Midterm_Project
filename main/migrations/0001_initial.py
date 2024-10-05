# Generated by Django 5.0.7 on 2024-10-05 03:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('island', models.CharField(max_length=255)),
                ('cuisine', models.CharField(max_length=255)),
                ('desc', models.TextField()),
            ],
        ),
    ]
