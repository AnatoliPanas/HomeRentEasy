from django.db.models import Q, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.filters.filter_rent import RentFilter
from applications.permissions.permissions import IsOwnerOrReadOnly
from applications.rent.models.locations import Address
from applications.rent.models.rent import Rent
from applications.rent.serializers import (RentListSerializer,
                                           RentCreateSerializer,
                                           RentSwitchActiveSerializer,
                                           RentDetailSerializer,

                                           AddressListSerializer,
                                           AddressCreateSerializer)


class AddressListCreateGenericAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AddressListSerializer
        return AddressCreateSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['postal_code', 'country', 'city', 'street']
    search_fields = ['country', 'city', 'street']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RentListCreateGenericAPIView(ListCreateAPIView):
    # queryset = Rent.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    ordering = ['-avg_rating']
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = RentFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'avg_rating', 'cn_views']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentListSerializer
        return RentCreateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Rent.objects.select_related('address', 'owner').filter(Q(owner=user) | Q(is_active=True))
        return queryset

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        address = serializer.validated_data.get('address')

        rent = Rent.objects.filter(
            title=title,
            address=address,
            is_deleted=False
        )

        if rent.exists():
            raise PermissionDenied(
                f"Такое объявление уже подано"
            )

        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Объявление успешно создано',
            'data': response.data
        }, status=status.HTTP_201_CREATED)


class RentDetailUpdateDeleteGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Rent.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'rent_id'

    def get_queryset(self):
        return Rent.objects.select_related('owner', 'address')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentDetailSerializer
        else:
            return RentCreateSerializer

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user and not obj.is_active:
            raise PermissionDenied("Объявление не доступно")
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.set_cn_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        # serializer = RentCreateSerializer(instance=instance, data=data, partial=True)
        serializer = self.get_serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RentSwitchActiveAPIView(APIView):
    def patch(self, request, rent_id):
        rent = get_object_or_404(Rent, id=rent_id, is_deleted=False)
        rent.is_active = not rent.is_active
        rent.save()
        serializer = RentSwitchActiveSerializer(rent)
        return Response(serializer.data, status=status.HTTP_200_OK)
