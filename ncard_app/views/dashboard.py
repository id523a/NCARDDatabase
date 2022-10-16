from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import login_required

@login_required(message=None)
def dashboard(request):
    return render(request, 'events/dashboard.html', {})
