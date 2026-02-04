from django.urls import path

from apps.seller import views

app_name = 'seller'

urlpatterns = [
    path('', views.SellerListCreateAPIView.as_view(), name='list-create'),
    path('<slug:slug>/', views.SellerRetrieveAPIView.as_view(), name='retrieve'),
]
