from rest_framework import serializers

from apps.product.models import Product, ProductImage
from apps.seller.serializers import SellerListSerializer
from apps.product.fields import MultiLookupHyperlinkedIdentityField


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        exclude = ('id', 'product')


class ProductDetailSerializer(serializers.ModelSerializer):

    seller = SellerListSerializer()
    primary_image = ProductImageSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):

    primary_image = ProductImageSerializer()
    retrieve = MultiLookupHyperlinkedIdentityField(
        view_name='api:product:retrieve',
        lookup_fields={'slug': 'product_slug', 'seller__slug': 'seller_slug'},
    )

    class Meta:
        model = Product
        exclude = ('id', 'seller')
