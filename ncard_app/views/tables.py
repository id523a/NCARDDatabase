from django.shortcuts import render
from ncard_app.models import Organisation, Person
from .decorators import login_required
from django.http import JsonResponse

@login_required
def list_people(request):
    people_list = Person.objects.all()
    return render(request, 'tables/people.html', {'people_list': people_list})

@login_required
def list_organisations(request):
    organisations_list = Organisation.objects.all()
    return render(request, 'tables/organisations.html', {'organisations_list': organisations_list})
