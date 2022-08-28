from django.shortcuts import render, HttpResponse, redirect
from app01test.models import NcardInfo


# Create your views here.
def index(request):
    return HttpResponse("hello");


def showList(request):
    # 默认在当前目录下的templates下找
    name = "test";
    return render(request, "user.html", {"n1": name});


def info_list(request):
    data_list = NcardInfo.objects.all()
    print(data_list)
    return render(request, "user.html", {"datalist": data_list})


def info_add(request):
    if request.method == "GET":
        return render(request, "info_add.html");
    else:
        title = request.POST.get("title")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        location = request.POST.get("location")
        primary_organisation = request.POST.get("primary_organisation")
        other_organisation = request.POST.get("other_organisation")
        email = request.POST.get("Phone")
        phone = request.POST.get("Email")
        nCARD_collaborator = request.POST.get("NCARD_collaborator")
        project = request.POST.get("Project")
        twitter_handle = request.POST.get("Twitter_handle")
        profile_link = request.POST.get("Profile_link")

        NcardInfo.objects.create(title=title, firstname=firstname, lastname=lastname, location=location,
                                 primary_organisation=primary_organisation, other_organisation=other_organisation,
                                 Email=email, Phone=phone, NCARD_collaborator=nCARD_collaborator, Project=project,
                                 Twitter_handle=twitter_handle, Profile_link=profile_link)
        return redirect("/info/")


def info_delete(request):
    inId = request.GET.get('id');
    NcardInfo.objects.filter(id=inId).delete();
    return redirect("/info/")


def info_update(request,id):
    if request.method=='GET':
        info=NcardInfo.objects.filter(id=id).first

        return render(request,"info_update.html",{'data':info});

    title = request.POST.get("title")
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    location = request.POST.get("location")
    primary_organisation = request.POST.get("primary_organisation")
    other_organisation = request.POST.get("other_organisation")
    email = request.POST.get("Phone")
    phone = request.POST.get("Email")
    nCARD_collaborator = request.POST.get("NCARD_collaborator")
    project = request.POST.get("Project")
    twitter_handle = request.POST.get("Twitter_handle")
    profile_link = request.POST.get("Profile_link")
    NcardInfo.objects.filter(id=id).update(title=title, firstname=firstname, lastname=lastname, location=location,
                                 primary_organisation=primary_organisation, other_organisation=other_organisation,
                                 Email=email, Phone=phone, NCARD_collaborator=nCARD_collaborator, Project=project,
                                 Twitter_handle=twitter_handle, Profile_link=profile_link)

    return redirect("/info/")