import random

from api.models import Car, Location
from core.celery import app


@app.task
def update_locations_car():
    locations = Location.objects.all()
    cars_to_update = []
    for car in Car.objects.all():
        car.current_location = random.choice(locations)
        cars_to_update.append(car)
    return Car.objects.bulk_update(objs=cars_to_update, fields=['current_location'], batch_size=1000)
