from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Q
from django.utils import timezone
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'full_name',
        'role_colored',
        'is_active',
        'is_staff',
        'phone',
        'birth_day',
        'date_joined',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'role',
        'date_joined',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone'
    )

    ordering = ('-date_joined',)

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (_('Учетные данные'), {
            'fields': ('username', 'email', 'password')
        }),
        (_('Личная информация'), {
            'fields': (
                'first_name',
                'last_name',
                'phone',
                'birth_day',
                'role'
            )
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Важные даты'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'role',
                'first_name',
                'last_name',
                'is_active',
                'is_staff'
            ),
        }),
    )

    actions = ['activate_users', 'deactivate_users', 'make_staff']

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "-"

    full_name.short_description = _('Полное имя')
    full_name.admin_order_field = 'first_name'

    def role_colored(self, obj):
        colors = {
            'ADMIN': '#FF0000',
            'LESSOR': '#008000',
            'LESSEE': '#0000FF',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.role, 'black'),
            obj.get_role_display()
        )

    role_colored.short_description = _('Роль')
    role_colored.admin_order_field = 'role'

    @admin.action(description=_('Активировать выбранных пользователей'))
    def activate_users(self, request, queryset):

        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            _(f'Активировано пользователей: {updated}')
        )

    @admin.action(description=_('Деактивировать выбранных пользователей'))
    def deactivate_users(self, request, queryset):
        admins_count = User.objects.filter(role='ADMIN', is_active=True).count()
        selected_admins = queryset.filter(role='ADMIN', is_active=True).count()

        if admins_count == selected_admins:
            self.message_user(
                request,
                _('Нельзя деактивировать всех администраторов!'),
                level='ERROR'
            )
            return

        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            _(f'Деактивировано пользователей: {updated}')
        )

    @admin.action(description=_('Назначить персоналом'))
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(
            request,
            _(f'Назначено персоналом: {updated}')
        )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            terms = search_term.split()
            if len(terms) > 1:
                queryset |= self.model.objects.filter(
                    Q(first_name__icontains=terms[0]) &
                    Q(last_name__icontains=terms[1])
                )
            else:
                queryset |= self.model.objects.filter(
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term)
                )
        return queryset, use_distinct

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return self.readonly_fields + ('role',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            if not obj.is_superuser and obj.role == 'ADMIN':
                obj.is_staff = True
        super().save_model(request, obj, form, change)
