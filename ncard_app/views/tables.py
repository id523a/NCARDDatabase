from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from ncard_app.models import Award, Organisation, Person
from .decorators import login_required
from django.http import JsonResponse

@login_required
def list_people(request):
    people_list = Person.objects.all()
    paginator = Paginator(people_list, 10)
    page = request.GET.get('page',1)
    try:
        people = paginator.page(page)
    except PageNotAnInteger:
        people = paginator.page(1)
    except EmptyPage:
        people = paginator.page(paginator.num_pages)
    context = {
        'people': people,
    }
    return render(request, 'tables/people.html', context)

@login_required
def list_organisations(request):
    organisations_list = Organisation.objects.all()
    paginator = Paginator(organisations_list, 10)
    page = request.GET.get('page',1)
    try:
        organisations = paginator.page(page)
    except PageNotAnInteger:
        organisations = paginator.page(1)
    except EmptyPage:
        organisations = paginator.page(paginator.num_pages)
    context = {
        'organisations': organisations,
    }
    return render(request, 'tables/organisations.html', context)

@login_required
def list_awards(request):
    awards_list = Award.objects.all()
    paginator = Paginator(awards_list, 10)
    page = request.GET.get('page',1)
    try:
        awards = paginator.page(page)
    except PageNotAnInteger:
        awards = paginator.page(1)
    except EmptyPage:
        awards = paginator.page(paginator.num_pages)
    context = {
        'awards': awards,
    }
    return render(request, 'tables/awards.html', context)