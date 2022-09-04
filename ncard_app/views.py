from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ncard_app.models import Award
from django.contrib import messages

def index(request):
    template_context = {
        'value': 123,
    }
    return render(request, 'events/index.html', template_context)

def home(request):
    if not request.user.is_authenticated:
        messages.error(request, ("Please login to access this page."))
        return redirect('login')
    return render(request, 'events/home.html', {})

def test_show(request):
    if request.method == "GET":
        return render(request, "test01.html")

    type = request.POST.get("type")
    agency = request.POST.get("agency")
    name = request.POST.get("name")
    status = request.POST.get("status")
    start_date=request.POST.get("startDate")
    end_date=request.POST.get("endDate")
    given_name = request.POST.get("givenName")
    surname=request.POST.get("surname")
    noYear=request.POST.get("noYear")


    search_dict = dict()

    if noYear:
        search_dict["noYear"] = noYear
    if type:
        search_dict["type"] = type

    if status:
       search_dict["status"] = status


    data = Award.objects.filter(**search_dict)
    # print(data)

    if name:
        data=data.filter(name__icontains=name)
    if agency:
        data=data.filter(agency__name__icontains=agency)
    if start_date:
        data = data.filter(year__gte=start_date)
    if end_date:
        data=data.filter(year__lt=end_date)
        

    if given_name:
        data=data.filter(recipients__given_name__icontains=given_name)
    if surname:
        data=data.filter(recipients__surname__icontains=surname)

    return render(request, "test01.html", {"n1":data})
