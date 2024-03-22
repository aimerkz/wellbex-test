import random
import re
import string

from typing import List

from api.models import Car, Location

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('cnt_cars', type=int, help='Count for creating cars')

    def handle(self, *args, **kwargs):
        cnt_cars = kwargs.get('cnt_cars')
        locations = self.get_location_random_instanses(cnt_cars)
        self.create_cars(locations)

    @staticmethod
    def get_location_random_instanses(cnt_cars: int) -> List[Location]:
        location_random_instances = []
        locations = Location.objects.all()
        for _ in range(cnt_cars):
            location = random.choice(locations)
            location_random_instances.append(location)
        return location_random_instances

    @staticmethod
    def generate_random_unique_number() -> str:
        regex_pattern = r'[0-9]{4}[A-Z]$'
        while True:
            random_number = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5))
            if re.fullmatch(regex_pattern, random_number):
                return random_number

    def create_cars(self, locations: List[Location]):
        for lct in locations:
            Car.objects.create(
                unique_number=self.generate_random_unique_number(),
                current_location=lct,
                carrying=random.randint(1, 1000)
            )
        self.stdout.write(self.style.SUCCESS('Cars created successfully'))
