from django.shortcuts import render
from ncard_app.models import Person
from .decorators import login_required
from django.http import JsonResponse

@login_required
def list_people(request):
    people_list = Person.objects.all()
    return render(request, 'tables/people.html', {'people_list': people_list})

def save_people(request):
    id = request.POST.get("id")
    type = request.POST.get("type")
    value = request.POST.get("value")
    person=Person.objects.get(id=id)
    if type == "title":
        person.title = value
    if type == "given_name":
        person.given_name = value
    if type == "middle_name":
        person.middle_name = value
    if type == "surname":
        person.surname = value
    person.save()
    return JsonResponse({"success":"Update"})
