from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.user.models import User, Address, BetterAuthSession


class BetterAuthSessionInline(admin.TabularInline):
    extra = 1
    model = BetterAuthSession
    readonly_fields = ('token', 'userAgent', 'ipAddress', 'impersonatedBy', 'expiresAt')


class AddressInline(admin.TabularInline):
    extra = 1
    model = Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    ordering = ('name',)
    list_filter = ('email_verified',)
    search_fields = ('name', 'email')
    readonly_fields = ('last_login', 'avatar')
    inlines = (AddressInline, BetterAuthSessionInline)
    list_display = ('name', 'email', 'is_staff', 'email_verified')

    def avatar(self, obj: User) -> str:
        if obj.image:
            return format_html('<img src="{src}" style="width: 250px; height: 250px;" />', src=obj.image)
        return format_html('<span style="color: red;">{msg}</span>', msg=_('No avatar'))

    avatar.short_description = _('Avatar')

    add_fieldsets = (
        (
            None,
            {'classes': ('wide',), 'fields': ('email', 'usable_password', 'password1', 'password2')},
        ),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Image'), {'fields': ('image', 'avatar')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
