from rest_framework import serializers

from api.models import Goods, Location, Car


class GoodsCreateSerializer(serializers.Serializer):
    zip_code_pick_up = serializers.IntegerField(required=True)
    zip_code_delivery = serializers.IntegerField(required=True)
    weight = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=999)


class NestedLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('city', 'state', 'zip_code', 'latitude', 'longitude')


class GoodsListSerializer(serializers.ModelSerializer):
    location_pick_up = NestedLocationSerializer()
    location_delivery = NestedLocationSerializer()
    number_of_nearby_cars = serializers.IntegerField()

    class Meta:
        model = Goods
        fields = ('weight', 'description', 'location_pick_up', 'location_delivery', 'number_of_nearby_cars')


class CarUpdateSerializer(serializers.ModelSerializer):
    zip_code = serializers.IntegerField(required=True)

    class Meta:
        model = Car
        fields = ('unique_number', 'zip_code', 'carrying')
