from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('seller/', include('apps.seller.urls')),
]
