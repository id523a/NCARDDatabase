from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ncard_app.models import Award, Person
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

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ("Incorrect username or password, please try again."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully."))
    return redirect('login')

def all_people(request):
    if not request.user.is_authenticated:
        messages.error(request, ("Please login to access this page."))
        return redirect('login')
    people_list = Person.objects.all()
    return render(request, 'tables/people.html', {'people_list': people_list})

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
