from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404,
                                     RetrieveAPIView,
                                     ListAPIView)
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
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
    queryset = Rent.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = RentFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentListSerializer
        return RentCreateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Rent.objects.all()

        return queryset.filter(Q(owner=user) | Q(is_active=True))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RentDetailUpdateDeleteGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Rent.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'rent_id'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentDetailSerializer
        else:
            return RentCreateSerializer


    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user and not obj.is_active:
            raise PermissionDenied("Объявление не доступно")
        self.check_object_permissions(self.request, obj)
        return obj

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.request.user == queryset.db.owner:
    #         return Rent.objects.filter(
    #             is_active=True
    #         )
    #     return queryset

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
