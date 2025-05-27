from django_filters import rest_framework as filters
from applications.rent.models.rent import Rent

class RentFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    rooms_min = filters.NumberFilter(field_name='rooms_count', lookup_expr='gte')
    rooms_max = filters.NumberFilter(field_name='rooms_count', lookup_expr='lte')
    city = filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    room_type = filters.CharFilter(field_name='room_type', lookup_expr='exact')
    owner  = filters.CharFilter(field_name='owner__username', lookup_expr='icontains')


    class Meta:
        model = Rent
        fields = []