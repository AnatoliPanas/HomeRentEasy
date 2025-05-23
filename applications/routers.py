from django.urls import path

from applications.bookings.views import BookingListCreateGenericAPIView
from applications.rent.views import (RentListCreateGenericAPIView,
                                     RentDetailUpdateDeleteGenericAPIView,
                                     RentSwitchActiveAPIView,
                                     AddressListCreateGenericAPIView
                                     )

from applications.users.views import (RegisterUserAPIView,
                                      LogInAPIView,
                                      LogOutAPIView)

urlpatterns = [
    path('rent/', RentListCreateGenericAPIView.as_view()),
    path('rent/<int:rent_id>/', RentDetailUpdateDeleteGenericAPIView.as_view()),
    path('rent/<int:rent_id>/switch-active/', RentSwitchActiveAPIView.as_view()),

    path('bookings/', BookingListCreateGenericAPIView.as_view()),

    path('address/', AddressListCreateGenericAPIView.as_view()),

    path('auth-register/', RegisterUserAPIView.as_view()),
    path('auth-login/', LogInAPIView.as_view()),
    path('auth-logout/', LogOutAPIView.as_view()),
]
