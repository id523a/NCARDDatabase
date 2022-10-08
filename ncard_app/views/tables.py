from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from ncard_app.models import Organisation, Person
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
    return render(request, 'tables/organisations.html', {'organisations_list': organisations_list})
