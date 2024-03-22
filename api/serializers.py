from rest_framework import serializers


class GoodsCreateSerializer(serializers.Serializer):
    zip_code_pick_up = serializers.IntegerField(required=True)
    zip_code_delivery = serializers.IntegerField(required=True)
    weight = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=999)
