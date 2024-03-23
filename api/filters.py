from django_filters import rest_framework as filters

from api.models import Goods


class WeightFilter(filters.FilterSet):
    min_weight = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    max_weight = filters.NumberFilter(field_name='weight', lookup_expr='lte')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ()
