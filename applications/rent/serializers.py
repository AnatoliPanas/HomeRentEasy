from rest_framework import serializers

from applications.rent.models.rent import Rent
from applications.rent.models.locations import Address


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'country',
            'city',
            'street',
            'house_number',
            'apartment_number',
            'postal_code'
        ]
        extra_kwargs = {'house_number': {'required': False},
                        'apartment_number': {'required': False}}


class RentListSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField(read_only=True)

    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rent
        fields = '__all__'


class RentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = [
            'title',
            'description',
            'address',
            'price',
            'rooms_count',
            'room_type',
            'is_active'
        ]
        extra_kwargs = {'is_active': {'write_only': True}}


class RentDetailSerializer(serializers.ModelSerializer):
    address = AddressListSerializer(read_only=True, allow_null=True)
    owner = serializers.StringRelatedField(read_only=True)

    # address = serializers.StringRelatedField()
    # address = serializers.SlugRelatedField(
    #     slug_field='country',
    #     read_only=True
    # )

    class Meta:
        model = Rent
        fields = [
            'title',
            'description',
            'address',
            'price',
            'rooms_count',
            'room_type',
            'is_active',
            'created_at',
            'owner'
        ]

class RentSwitchActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ['is_active']
