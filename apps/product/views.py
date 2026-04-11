from rest_framework import generics

from apps.product.models import Product
from apps.product.serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(generics.ListAPIView):

    search_fields = ('name',)
    ordering_fields = ('price',)
    serializer_class = ProductListSerializer

    def get_queryset(self):
        seller_slug = self.kwargs['seller_slug']
        return Product.objects.filter(seller__slug=seller_slug).select_related('primary_image').order_by('-added_on')


class ProductRetrieveView(generics.RetrieveAPIView):

    lookup_field = 'slug'
    lookup_url_kwarg = 'product_slug'
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        seller_slug = self.kwargs['seller_slug']
        return (
            Product.objects.filter(seller__slug=seller_slug)
            .prefetch_related('images')
            .select_related('seller', 'primary_image')
        )
