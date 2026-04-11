from rest_framework import serializers
from django.shortcuts import get_object_or_404

from apps.seller.models import Seller, SellerPageText


class CurrentSellerDefault:
    requires_context = True

    def __call__(self, serializer_field):
        # Get seller slug from URL kwargs
        slug: str = serializer_field.context['view'].kwargs.get('slug')
        return get_object_or_404(Seller, slug=slug)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class SellerCreateSerializer(serializers.ModelSerializer):

    managed_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Seller
        exclude = ('slug',)


class SellerListSerializer(serializers.ModelSerializer):

    products = serializers.HyperlinkedIdentityField(
        lookup_field='slug',
        view_name='api:product:list',
        lookup_url_kwarg='seller_slug',
    )
    retrieve = serializers.HyperlinkedIdentityField(
        lookup_field='slug',
        lookup_url_kwarg='slug',
        view_name='api:seller:retrieve',
    )

    class Meta:
        model = Seller
        exclude = ('id', 'managed_by')


class SellerPageTextSerializer(serializers.ModelSerializer):

    seller = serializers.HiddenField(default=CurrentSellerDefault())

    class Meta:
        model = SellerPageText
        exclude = ('id',)


class SellerDetailSerializer(serializers.ModelSerializer):

    texts = SellerPageTextSerializer(many=True)
    products = serializers.HyperlinkedIdentityField(
        lookup_field='slug',
        view_name='api:product:list',
        lookup_url_kwarg='seller_slug',
    )

    class Meta:
        model = Seller
        exclude = ('id', 'managed_by')
