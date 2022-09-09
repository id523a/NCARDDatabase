from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import login_required

@login_required
def home(request):
    return render(request, 'events/home.html', {})
