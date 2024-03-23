from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response

from api.models import Goods, Car
from api.serializers import GoodsCreateSerializer, GoodsListSerializer, CarUpdateSerializer
from api.services import GoodsRepo, get_goods_with_number_of_nearby_cars, get_detail_goods_qs, CarRepo


class CreateGoodsView(ListCreateAPIView):

    serializer_class = GoodsCreateSerializer
    queryset = Goods.objects.all()
    http_method_names = ['get', 'post']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return GoodsListSerializer
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        GoodsRepo(
            serializer.validated_data.pop('zip_code_pick_up'),
            serializer.validated_data.pop('zip_code_delivery'),
            serializer.validated_data.pop('weight'),
            serializer.validated_data.pop('description')
        ).create_goods()
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.select_related('location_pick_up', 'location_delivery')
        res = get_goods_with_number_of_nearby_cars(queryset)
        serializer = self.get_serializer(res, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RetrieveGoodsView(RetrieveAPIView):

    http_method_names = ['get']
    serializer_class = GoodsListSerializer
    queryset = Goods.objects.all()
    lookup_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        instance_qs = get_detail_goods_qs(kwargs.get('id'))
        res = get_goods_with_number_of_nearby_cars(instance_qs)
        serializer = self.get_serializer(res.first())
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UpdateCarView(UpdateAPIView):

    http_method_names = ['put']
    serializer_class = CarUpdateSerializer
    queryset = Car.objects.all()
    lookup_url_kwarg = 'id'

    def update(self, request, *args, **kwargs):
        car_instance = self.get_object()
        serializer = self.get_serializer(car_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        CarRepo(
            car_instance,
            serializer.validated_data.pop('zip_code'),
            serializer.validated_data.pop('unique_number'),
            serializer.validated_data.pop('carrying')
        ).update_car()
        return Response(status=status.HTTP_200_OK)
