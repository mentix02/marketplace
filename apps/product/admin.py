from django.contrib import admin

from apps.product.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    extra = 1
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('added_on',)
    inlines = (ProductImageInline,)
    list_display = ('name', 'price', 'seller', 'added_on')
    search_fields = ('name', 'description', 'seller__name')
