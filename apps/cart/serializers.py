from rest_framework import serializers

from apps.cart.models import CartItem
from apps.product.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductListSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'
