import csv
from django.core.management.base import BaseCommand
from search.models import (
    Restaurant,
)


class Command(BaseCommand):
    help = "Import restaurants from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        with open(csv_file, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                restaurant = Restaurant(
                    name=row["name"],
                    island=row["island"],
                    cuisine=row["cuisine"],
                    contacts=row["contacts"],
                    gmaps=row["gmaps"],
                )
                restaurant.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully imported {restaurant.name}")
                )
