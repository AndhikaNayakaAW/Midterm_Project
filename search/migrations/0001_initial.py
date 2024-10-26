# Generated by Django 5.1.1 on 2024-10-09 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
