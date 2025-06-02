from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.permissions.permissions import IsAdminOrAllowAny
from applications.users.models.user import User
from applications.users.serializers import RegisterUserSerializer, UserListSerializer, LoginSerializer
from applications.users.utils import set_jwt_cookies


class RegisterUserAPIView(ListCreateAPIView):
    queryset = User.objects.all()

    # permission_classes = [IsAdminOrAllowAny]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserListSerializer
        return RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response = Response(
            data={
                "message": "Пользователь успешно создан",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        set_jwt_cookies(response, user)
        return response


class LogInAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        # username = request.data.get('username')
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(data={"errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        password = request.data.get('password')
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return Response(
                data={
                    "error": "Неверные учетные данные",
                    "message": f"Пользователь с почтой: {email} не найден"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if not user:
            return Response(
                data={
                    "error": "Неверные учетные данные",
                    "message": "Проверьте правильность введенной почты и пароля"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                data={
                    "error": "Аккаунт неактивен",
                    "message": "Ваш аккаунт был деактивирован. Пожалуйста, свяжитесь с администратором."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        response = Response(
            data={
                "message": "Авторизация успешна",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            },
            status=status.HTTP_200_OK
        )

        set_jwt_cookies(response=response, user=user)

        return response


class LogOutAPIView(APIView):
    def post(self, request: Request) -> Response:
        response = Response(
            data={"message": f"Выход выполнен"},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
