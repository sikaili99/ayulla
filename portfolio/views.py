from django.http import HttpResponseNotFound
from .forms import CryptoForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Crypto
import requests


@login_required
def dashboard(request):
    user = request.user
    portfolio = user.portfolio.all()

    # TODO: Retrieve 24-hour price and percentage change for each cryptocurrency in the user's portfolio

    search_query = request.GET.get('search_query')
    if search_query:
        search_results = Crypto.objects.filter(name__icontains=search_query)
        return render(request, 'dashboard.html', {'cryptocurrencies': search_results, 'portfolio': portfolio, 'search_query': search_query})
    else:
        # Retrieve all cryptocurrencies from the database
        cryptocurrencies = Crypto.objects.all()
        return render(request, 'dashboard.html', {'cryptocurrencies': cryptocurrencies, 'portfolio': portfolio})


def add_crypto(request):
    if request.method == 'POST':
        form = CryptoForm(request.POST)
        if form.is_valid():
            crypto = form.save(commit=False)
            crypto.user = request.user
            crypto.save()
            return redirect('portfolio:dashboard')
    else:
        form = CryptoForm()
    return render(request, 'add_crypto.html', {'form': form})


def remove_crypto(request, crypto_id):
    try:
        crypto = Crypto.objects.get(pk=crypto_id)
    except Crypto.DoesNotExist:
        return HttpResponseNotFound("Crypto not found.")
    
    try:
        # TODO: Associate user with crypto wallet (Portfolio).
        portfolio = request.user.portfolio
        portfolio.remove(crypto)
    except AttributeError:
        crypto.delete()
        
    return redirect('portfolio:dashboard')

