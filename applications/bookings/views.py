from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from applications.bookings.choices.waiting_status import WaitingStatus
from applications.bookings.models import Booking
from applications.bookings.serializers import BookingListSerializer, BookingCreateSerializer
from applications.permissions.permissions import IsOwnerOrReadOnlyBooking
from applications.users.choices.role_type import RoleType


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
        if user.is_superuser:
            return queryset

        # print(user)
        # for booking in queryset[:5]:
        #     print(f"Lessee: {booking.lessee}, Rent owner: {booking.rent.owner}")
        return queryset.filter(Q(lessee=user) | Q(rent__owner=user))

    def perform_create(self, serializer):
        serializer.save(lessee=self.request.user)


class BookingDetailUpdateDeleteGenericAPIView(RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsOwnerOrReadOnlyBooking]
    lookup_url_kwarg = 'booking_id'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingListSerializer
        else:
            return BookingCreateSerializer

    def partial_update(self, request, *args, **kwargs):
        # print('patch', '==' * 100)
        instance = self.get_object()
        user = request.user
        data = request.data.copy()

        if 'status' not in data:
            raise PermissionDenied("Разрешено только изменение статуса")

        new_status = data.get('status')

        if new_status == WaitingStatus.CANCELLED.name:
            if instance.lessee != user:
                raise PermissionDenied("Вы не можете отменить чужое бронирование")
            if not instance.can_cancel():
                raise PermissionDenied("Отменить можно только подтвержденные бронирования"
                                       "и минимум за два дня до начала действия брони")
        elif new_status in [WaitingStatus.CONFIRMED.name, WaitingStatus.DECLINED.name]:
            if instance.status != WaitingStatus.PENDING.name:
                raise PermissionDenied("Подтверждать/отклонять можно только заявки в статусе 'В ожидании'")
            if instance.rent.owner != user:
                raise PermissionDenied("Только владелец объявления может изменить статус брони")
        else:
            raise ValidationError("Недопустимый статус")

        instance.status = new_status
        instance.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
