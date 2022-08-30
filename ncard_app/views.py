from django.shortcuts import render

def index(request):
    template_context = {
        'value': 123,
    }
    return render(request, 'events/index.html', template_context)