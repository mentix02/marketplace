from django.urls import path

from apps.product import views

app_name = 'product'

urlpatterns = [
    path('<slug:seller_slug>/', views.ProductListView.as_view(), name='list'),
    path('<slug:seller_slug>/<slug:product_slug>/', views.ProductRetrieveView.as_view(), name='retrieve'),
]
