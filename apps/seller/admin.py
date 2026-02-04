from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from apps.seller.models import Seller, SellerPageText


class SellerPageTextInline(OrderedTabularInline):
    extra = 1
    ordering = ('order',)
    model = SellerPageText
    readonly_fields = ('order', 'move_up_down_links')
    fields = ('content', 'title', 'image', 'move_up_down_links')


@admin.register(Seller)
class SellerAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    ordering = ('-added_on',)
    list_filter = ('added_on',)
    inlines = (SellerPageTextInline,)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'managed_by__username')
    list_display = ('name', 'managed_by', 'added_on')
