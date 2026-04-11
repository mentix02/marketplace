from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView

from apps.user.permissions import IsAdminOrReadOnly
from apps.seller.models import Seller, SellerPageText
from apps.seller.serializers import (
    SellerListSerializer,
    SellerCreateSerializer,
    SellerDetailSerializer,
    SellerPageTextSerializer,
)


class SellerListCreateAPIView(ListCreateAPIView):

    name = 'Seller List Create API'

    # Filters
    ordering_fields = ()
    search_fields = ('name',)
    filterset_fields = ('state', 'city')

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Seller.objects.all().order_by('?')

    def get_serializer_class(self):
        return SellerCreateSerializer if self.request.method == 'POST' else SellerListSerializer


class SellerRetrieveAPIView(RetrieveAPIView):

    name = 'Seller Retrieve API'

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = SellerDetailSerializer
    queryset = Seller.objects.prefetch_related('texts').all()


class SellerTextsListCreateAPIView(ListCreateAPIView):

    name = 'Seller Texts List Create API'

    permission_classes = (IsAdminUser,)
    serializer_class = SellerPageTextSerializer
    queryset = SellerPageText.objects.all().order_by('order')

    def get_queryset(self):
        slug: str = self.kwargs['slug']
        return self.queryset.filter(seller__slug=slug)
