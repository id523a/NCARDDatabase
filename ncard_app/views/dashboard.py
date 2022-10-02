from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'events/dashboard.html', {})
