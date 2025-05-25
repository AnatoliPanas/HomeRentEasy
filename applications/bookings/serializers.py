import datetime

from django.utils import timezone
from rest_framework import serializers

from applications.bookings.models import Booking


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'rent',
            'start_date',
            'end_date',
        ]

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date and start_date < timezone.now().date():
            raise serializers.ValidationError(
                {"start_date": f"{start_date=} не может быть в прошлом"}
            )

        if end_date and end_date < timezone.now().date():
            raise serializers.ValidationError(
                {"end_date": f"{end_date=} не может быть в прошлом"}
            )

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                {"start_date": f"{start_date=} должна быть меньше {end_date=}"}
            )

        return attrs
