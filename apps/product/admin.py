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

    def get_form(self, request, obj=None, **kwargs):
        request._object = obj
        return super().get_form(request, obj, **kwargs)

    # noinspection PyProtectedMember, PyUnresolvedReferences
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'primary_image' and request._object:
            product = request._object
            kwargs['queryset'] = product.images.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
