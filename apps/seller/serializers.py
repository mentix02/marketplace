from rest_framework import serializers

from apps.seller.models import Seller, SellerPageText


class SellerCreateSerializer(serializers.ModelSerializer):

    managed_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Seller
        exclude = ('slug',)


class SellerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        exclude = ('managed_by',)


class SellerPageTextSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('seller',)
        model = SellerPageText


class SellerDetailSerializer(serializers.ModelSerializer):

    texts = SellerPageTextSerializer(many=True)

    class Meta:
        model = Seller
        exclude = ('managed_by',)
