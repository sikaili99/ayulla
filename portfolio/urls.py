from django.urls import path
from .views import add_crypto, dashboard, remove_crypto

app_name = 'portfolio'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add_crypto/', add_crypto, name='add_crypto'),
    path('remove_crypto/<int:crypto_id>/', remove_crypto, name='remove_crypto')
]
