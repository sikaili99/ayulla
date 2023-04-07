from django.urls import path
from .views import index, login_view, RegisterView, logout_view

app_name = 'accounts'
urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='signup'),
]
