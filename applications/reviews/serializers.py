from rest_framework import serializers

from applications.reviews.models.review import Review


class ReviewListSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField()
    rent = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'rent',
            'rating',
            'comment',
        ]

    # def validate(self, attrs):
    #     user = self.context['request'].user
    #     rent = attrs.get('rent')
    #     if Review.objects.filter(reviewer=user, rent=rent).exists():
    #         raise serializers.ValidationError("Вы уже оставили отзыв на это объявление.")
    #     return attrs
