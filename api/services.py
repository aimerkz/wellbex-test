from api.exceptions import LocationNotFoundException
from api.models import Location, Goods


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


def get_location_by_zip_code(zip_code: int) -> Location:
    try:
        return Location.objects.get(zip_code=zip_code)
    except Location.DoesNotExist:
        raise LocationNotFoundException()
