from django.shortcuts import render
from ncard_app.models import Organisation, Person
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
    fields = {
            "title", 
            "given_name",
            "middle_name",
            "surname",
            # "email",
            # "email2",
            # "phone_office",
            # "phone_mobile",
            # "phone_home",
            # "cre_role",
            # "ncard_relation",
            # "project",
            # "display_on_website",
            # "profile_url",
            # "orcid_id",
            # "scopus_id",
            # "wos_researcher_id",
            # "google_scholar",
            # "researchgate",
            # "loop_profile",
            # "linkedin",
            # "twitter",
            # "employers",
            # "location",
            # "organisation_primary",
            # "organisation_other",
            # "clinician",
            # "notes",
            # "research_focus"
    }
    if type in fields:
        setattr(person, type, value)
        person.save()
    return JsonResponse({"success":"Update"})


@login_required
def list_organisations(request):
    organisations_list = Organisation.objects.all()
    return render(request, 'tables/organisations.html', {'organisations_list': organisations_list})

def save_organisations(request):
    id = request.POST.get("id")
    type = request.POST.get("type")
    value = request.POST.get("value")
    organisation=Organisation.objects.get(id=id)
    if type == "name":
        organisation.name = value
    if type == "primary_contact":
        organisation.primary_contact = value
    if type == "phone":
        organisation.phone = value
    if type == "website":
        organisation.website = value
    if type == "twitter_handle":
        organisation.twitter_handle = value
    if type == "type":
        organisation.type = value
    organisation.save()
    return JsonResponse({"success":"Update"})
