from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from decimal import Decimal
from django.contrib.admin import SimpleListFilter

from applications.rent.models import Rent, Address


class PriceRangeFilter(SimpleListFilter):
    title = _('Диапазон цен')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):

        return (
            ('0-50', '0€ - 50€'),
            ('51-100', '51€ - 100€'),
            ('101-200', '101€ - 200€'),
            ('201-500', '201€ - 500€'),
            ('501+', '501€ и выше'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        if self.value() == '501+':
            return queryset.filter(price__gte=501)

        start, end = map(int, self.value().split('-'))
        return queryset.filter(price__gte=start, price__lte=end)


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price_display',
        'room_type',
        'rooms_count',
        'rating_display',
        'views_display',
        'owner_link',
        'is_active',
        'created_at',
    )

    list_filter = [
        'is_active',
        'is_deleted',
        'room_type',
        PriceRangeFilter,
    ]

    search_fields = (
        'title',
        'description',
        'address__city',
        'address__street',
        'owner__username',
    )

    ordering = (
        '-created_at',
        '-avg_rating',
        'price',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'deleted_at',
        'avg_rating',
        'cn_views',
    )

    def price_display(self, obj):
        return f"{obj.price} €"

    price_display.short_description = _('Цена')
    price_display.admin_order_field = 'price'

    def rating_display(self, obj):
        return format_html('⭐ {}', obj.avg_rating)

    rating_display.short_description = _('Рейтинг')
    rating_display.admin_order_field = 'avg_rating'

    def views_display(self, obj):
        return format_html('👁 {}', obj.cn_views)

    views_display.short_description = _('Просмотры')
    views_display.admin_order_field = 'cn_views'

    def owner_link(self, obj):
        if obj.owner:
            return format_html(
                '<a href="/admin/users/user/{}/change/">{}</a>',
                obj.owner.id,
                obj.owner.username
            )
        return "-"

    owner_link.short_description = _('Владелец')
    owner_link.admin_order_field = 'owner__username'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'full_address',
        'country',
        'city',
        'postal_code',
        'owner_link',
        'created_at',
    )

    list_filter = (
        'country',
        'city',
        'created_at',
    )

    search_fields = (
        'country',
        'city',
        'street',
        'house_number',
        'apartment_number',
        'postal_code',
        'owner__username',
    )

    ordering = (
        '-created_at',
        'country',
        'city',
    )

    readonly_fields = ('created_at',)

    fieldsets = (
        (_('Адрес'), {
            'fields': (
                'country',
                'city',
                'street',
                'house_number',
                'apartment_number',
                'postal_code',
            )
        }),
        (_('Дополнительно'), {
            'fields': (
                'owner',
                'created_at',
            )
        }),
    )

    def full_address(self, obj):
        address_parts = [
            obj.street,
            obj.house_number,
            f"кв. {obj.apartment_number}" if obj.apartment_number else None
        ]
        return format_html(
            '<div style="min-width: 200px">{}</div>',
            ', '.join(filter(None, address_parts))
        )

    full_address.short_description = _('Адрес')

    def owner_link(self, obj):
        if obj.owner:
            return format_html(
                '<a href="/admin/users/user/{}/change/">{}</a>',
                obj.owner.id,
                obj.owner.username
            )
        return "-"

    owner_link.short_description = _('Владелец')
    owner_link.admin_order_field = 'owner__username'
