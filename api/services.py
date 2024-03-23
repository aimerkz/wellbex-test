from typing import List

from api.exceptions import LocationNotFoundException, GoodsNotFoundException
from api.models import Location, Goods, Car

from django.db.models import F, IntegerField, QuerySet, Value
from django.db.models.functions import JSONObject

from geopy.distance import geodesic


class GoodsRepo:

    def __init__(self, zip_code_pick_up: int, zip_code_delivery: int, weight: int, description: str | None):
        self.zip_code_pick_up = zip_code_pick_up
        self.zip_code_delivery = zip_code_delivery
        self.weight = weight
        self.description = description

    def create_goods(self) -> Goods:
        location_pick_up = get_location_by_zip_code(self.zip_code_pick_up)
        location_delivery = get_location_by_zip_code(self.zip_code_delivery)
        return Goods.objects.create(
            location_pick_up=location_pick_up,
            location_delivery=location_delivery,
            weight=self.weight,
            description=self.description
        )


def get_detail_goods_qs(pk: int) -> QuerySet[Goods]:
    goods_qs = Goods.objects.select_related('location_pick_up', 'location_delivery').filter(pk=pk)
    if not goods_qs.exists():
        raise GoodsNotFoundException()
    return goods_qs


def get_location_by_zip_code(zip_code: int) -> Location:
    try:
        return Location.objects.get(zip_code=zip_code)
    except Location.DoesNotExist:
        raise LocationNotFoundException()


def calculate_distance_for_filter_cars(
        ltd_1: float, lng_1: float,
        ltd_2: List[float], lng_2: List[float]
) -> List[float]:
    coordinates_sec = tuple((ltd, lng) for ltd, lng in zip(ltd_2, lng_2))
    res_list = []
    for coord in coordinates_sec:
        res_list.append(geodesic((ltd_1, lng_1), coord).miles)
    return res_list


def get_goods_with_number_of_nearby_cars(goods_qs: QuerySet[Goods]) -> QuerySet[Goods]:
    cars_for_annotate = Car.objects.all().annotate(
        car_latitude=F('current_location__latitude'),
        car_longitude=F('current_location__longitude'),
    ).values('car_latitude', 'car_longitude')

    annotate_goods_by_cars = goods_qs.annotate(
        car_location=JSONObject(
            car_latitude=Value([car['car_latitude'] for car in cars_for_annotate.values('car_latitude')]),
            car_longitude=Value([car['car_longitude'] for car in cars_for_annotate.values('car_longitude')])
        )
    )

    cns_nearby_cars = 0
    for good in annotate_goods_by_cars.values(
        'location_pick_up__latitude', 'location_pick_up__longitude', 'car_location'
    ):
        miles_res = calculate_distance_for_filter_cars(
            good['location_pick_up__latitude'],
            good['location_pick_up__longitude'],
            good['car_location']['car_latitude'],
            good['car_location']['car_longitude']
        )
        cns_nearby_cars += sum(1 for mile in miles_res if mile <= 450)

    return goods_qs.annotate(number_of_nearby_cars=Value(cns_nearby_cars, IntegerField()))
