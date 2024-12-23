# Generated by Django 5.0.7 on 2024-11-20 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0002_favorite_delete_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('island', models.CharField(max_length=63)),
                ('cuisine', models.CharField(max_length=63)),
                ('gmaps', models.TextField()),
                ('contacts', models.CharField(max_length=63)),
            ],
        ),
    ]
