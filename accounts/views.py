from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from accounts.models import CustomUser
from .forms import CustomLoginForm, CustomUserCreationForm


def index(request):
    return render(request, 'landing/index.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('portfolio:dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:index')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referral_code = self.request.GET.get('referral_code')
        if referral_code:
            context['referral_code'] = referral_code
        return context

    def form_valid(self, form):
        referral_code = self.request.POST.get('referral_code')
        if referral_code:
            try:
                referred_by = CustomUser.objects.get(
                    referral_code=referral_code)
                form.instance.referred_by = referred_by
                referred_by.balance += 10  # Or whatever bonus amount you want to give
                referred_by.save()
            except CustomUser.DoesNotExist:
                pass
        return super().form_valid(form)
