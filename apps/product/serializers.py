from rest_framework import serializers

from apps.product.models import Product, ProductImage
from apps.seller.serializers import SellerListSerializer


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = ProductImage


class ProductDetailSerializer(serializers.ModelSerializer):

    seller = SellerListSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):

    seller = SellerListSerializer()

    class Meta:
        model = Product
        fields = '__all__'
