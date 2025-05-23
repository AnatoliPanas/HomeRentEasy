from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from applications.bookings.models import Booking
from applications.bookings.serializers import BookingListSerializer, BookingCreateSerializer


class BookingListCreateGenericAPIView(ListCreateAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingListSerializer
        return BookingCreateSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['rent', 'start_date', 'end_date']
    search_fields = ['rent', 'start_date']
    ordering_fields = ['start_date', 'end_date']

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.all()
        # print(user)
        # for booking in queryset[:5]:
        #     print(f"Lessee: {booking.lessee}, Rent owner: {booking.rent.owner}")

        return queryset.filter(Q(lessee=user) | Q(rent__owner=user))

    def perform_create(self, serializer):
        serializer.save(lessee=self.request.user)
