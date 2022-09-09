from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    template_context = {
        'value': 123,
    }
    return render(request, 'events/index.html', template_context)
