from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.models import Goods
from api.serializers import GoodsCreateSerializer
from api.services import GoodsRepo


class CreateGoodsView(CreateAPIView):

    serializer_class = GoodsCreateSerializer
    queryset = Goods.objects.all()
    http_method_names = ['post']

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
