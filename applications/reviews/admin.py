from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from applications.reviews.models.review import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'rent_title',
        'reviewer_info',
        'rating_stars',
        'short_comment',
        'created_at',
    )

    list_filter = [
        'rating',
        'created_at',
        ('reviewer', admin.RelatedOnlyFieldListFilter),
        ('rent', admin.RelatedOnlyFieldListFilter),
    ]

    search_fields = (
        'reviewer__username',
        'reviewer__email',
        'rent__title',
        'comment',
    )

    ordering = (
        '-created_at',
        '-rating',
    )

    readonly_fields = ('created_at',)

    def rent_title(self, obj):
        return format_html(
            '<a href="/admin/rent/rent/{}/change/">{}</a>',
            obj.rent.id,
            obj.rent.title
        )
    rent_title.short_description = _('Объект аренды')
    rent_title.admin_order_field = 'rent__title'

    def reviewer_info(self, obj):
        return format_html(
            '<a href="/admin/users/user/{}/change/">{}</a>',
            obj.reviewer.id,
            obj.reviewer.username
        )
    reviewer_info.short_description = _('Рецензент')
    reviewer_info.admin_order_field = 'reviewer__username'

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #FFD700;">{}</span>',
            stars
        )
    rating_stars.short_description = _('Оценка')
    rating_stars.admin_order_field = 'rating'

    def short_comment(self, obj):
        if obj.comment:
            return (obj.comment[:50] + '...') if len(obj.comment) > 50 else obj.comment
        return '-'
    short_comment.short_description = _('Комментарий')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reviewer', 'rent')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.rent.set_avg_rating()