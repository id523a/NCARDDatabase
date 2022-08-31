from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    template_context = {
        'value': 123,
    }
    return render(request, 'events/index.html', template_context)

def home(request):
    if not request.user.is_authenticated:
        messages.success(request, ("Please login to access this page."))
        return redirect('login')
    return render(request, 'events/home.html', {})