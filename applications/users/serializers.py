import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from applications.users.choices.role_type import RoleType
from applications.users.models.user import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_staff',
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=RoleType.choices(),
        required=True
    )
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            're_password',
            'email',
            'role',
            'is_staff'
        ]

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')

        re_pattern = r'^[a-zA-Z]+$'

        if not email:
            raise serializers.ValidationError({'email': 'Это поле является обязательным.'})

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({'email': 'Пожалуйста, введите правильный адрес электронной почты.'})

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {"first_name": "Имя должно содержать только символы алфавита."}
            )

        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {"last_name": "Фамилия должна содержать только символы алфавита."}
            )

        # if role in [RoleType.LESSEE.name, RoleType.LESSOR.name] and is_staff:
        #     raise serializers.ValidationError({
        #         'is_staff': 'У данной роли нельзя установить is_staff=True'
        #     })
        #
        # if role in [RoleType.ADMIN.name, RoleType.MODERATOR.name] and not is_staff:
        #     raise serializers.ValidationError({
        #         'is_staff': 'У данной роли необходимо установить is_staff=True.'
        #     })

        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        if not password:
            raise serializers.ValidationError(
                {"password": "Это поле является обязательным."}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "Это поле является обязательным."}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Пароль не совпадает."}
            )

        return attrs

    def create(self, validated_data):
        role = validated_data.get('role')

        STAFF_ROLES = (RoleType.ADMIN.name, RoleType.MODERATOR.name)
        validated_data['is_staff'] = role in STAFF_ROLES

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user
