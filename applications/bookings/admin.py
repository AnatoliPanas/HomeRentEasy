from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from .models import Booking
from .choices.waiting_status import WaitingStatus


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'rent_title',
        'lessee_info',
        'date_range',
        'status_colored',
        'can_cancel_icon',
        'created_at',
    )

    list_filter = [
        'status',
        ('start_date', admin.DateFieldListFilter),
        ('end_date', admin.DateFieldListFilter),
        'created_at',
    ]

    search_fields = (
        'lessee__username',
        'lessee__email',
        'rent__title',
        'rent__description',
    )

    ordering = (
        '-created_at',
        'status',
        'start_date',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    def rent_title(self, obj):
        return format_html(
            '<a href="/admin/rent/rent/{}/change/">{}</a>',
            obj.rent.id,
            obj.rent.title
        )

    rent_title.short_description = _('Объект аренды')
    rent_title.admin_order_field = 'rent__title'

    def lessee_info(self, obj):
        return format_html(
            '<a href="/admin/users/user/{}/change/">{}</a>',
            obj.lessee.id,
            obj.lessee.username
        )

    lessee_info.short_description = _('Арендатор')
    lessee_info.admin_order_field = 'lessee__username'

    def date_range(self, obj):
        return format_html(
            '{} → {}',
            obj.start_date.strftime('%d.%m.%Y'),
            obj.end_date.strftime('%d.%m.%Y')
        )

    date_range.short_description = _('Период аренды')
    date_range.admin_order_field = 'start_date'

    def status_colored(self, obj):
        colors = {
            WaitingStatus.PENDING.name: '#FFA500',
            WaitingStatus.CONFIRMED.name: '#008000',
            WaitingStatus.CANCELLED.name: '#808080',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )

    status_colored.short_description = _('Статус')
    status_colored.admin_order_field = 'status'

    def can_cancel_icon(self, obj):
        if obj.can_cancel():
            return format_html(
                '<img src="/static/admin/img/icon-yes.svg" alt="True">'
            )
        return format_html(
            '<img src="/static/admin/img/icon-no.svg" alt="False">'
        )

    can_cancel_icon.short_description = _('Можно отменить')

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )

        try:
            search_date = timezone.datetime.strptime(search_term, '%d.%m.%Y').date()
            queryset |= self.model.objects.filter(
                start_date__lte=search_date,
                end_date__gte=search_date
            )
        except ValueError:
            pass

        return queryset, may_have_duplicates