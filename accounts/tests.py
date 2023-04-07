from unittest import TestCase
from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import CustomAuthenticationForm
from .views import login_view

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_get_login_view(self):
        url = reverse('accounts:login')
        request = self.factory.get(url)
        response = login_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertTrue(isinstance(response.context['form'], CustomAuthenticationForm))

    def test_invalid_login(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='password')
        url = reverse('accounts:login')
        request = self.factory.post(url, {'username': 'test@example.com', 'password': 'wrongpassword'})
        response = login_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertTrue(isinstance(response.context['form'], CustomAuthenticationForm))
        self.assertTrue(response.context['form'].errors['__all__'])


    def test_valid_login(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        url = reverse('accounts:login')
        request = self.factory.post(url, {'username': 'test@example.com', 'password': 'password'})
        response = login_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        user = authenticate(request, username='test@example.com', password='password')
        self.assertIsNotNone(user)
        self.assertEqual(user, request.user)
