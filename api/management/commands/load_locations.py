import csv

from api.models import Location

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to csv file with locations data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs.get('csv_file')
        self.load_locations(csv_file)

    def load_locations(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            locations = []
            for row in reader:
                locations.append(
                    Location(
                        city=row['city'],
                        state=row['state_name'],
                        zip_code=row['zip'],
                        latitude=row['lat'],
                        longitude=row['lng']
                    )
                )
            Location.objects.bulk_create(objs=locations, batch_size=1000)
        self.stdout.write(self.style.SUCCESS('Locations data loaded successfully'))
