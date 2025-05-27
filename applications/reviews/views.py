from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from applications.bookings.choices.waiting_status import WaitingStatus
from applications.bookings.models import Booking
from applications.reviews.models.review import Review
from applications.reviews.serializers import ReviewCreateSerializer, ReviewListSerializer


class ReviewCreateGenericAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        rent = serializer.validated_data.get('rent')
        user = self.request.user

        booking = Booking.objects.filter(lessee=user, rent=rent)
        if not booking.exists():
            raise PermissionDenied("Вы можете оставить отзыв только после бронирования этого объявления.")

        review = Review.objects.filter(reviewer=user, rent=rent)
        if review.exists():
            raise PermissionDenied("Вы уже оставили отзыв на это объявление")

        serializer.save(reviewer=self.request.user)

class ReviewListGenericAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]

    filterset_fields = ['rating', 'reviewer__username']
    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']


    def get_queryset(self):
        rent_id = self.kwargs.get('rent_id')
        queryset = Review.objects.filter(rent=rent_id)
        return queryset