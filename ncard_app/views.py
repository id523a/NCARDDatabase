from django.shortcuts import render
from ncard_app.models import Award
from  ncard_app import forms
from django.views import View
def index(request):
    template_context = {
        'value': 123,
    }
    return render(request, 'index.html', template_context)

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

class CbShow(View):
    # form=xx
    template_name = "test02.html"
    form = forms.AwardForm()

    def get(self, request, *args, **kwargs):
        self.form.SetAllRequired()

        return render(request, self.template_name, {"form": self.form});

    def post(self, request, *args, **kwargs):
        form = forms.AwardForm(request.POST)
        form.SetAllRequired()
        if form.is_valid():

            type = form.cleaned_data["award_type"]
            recipients = form.cleaned_data["recipients"].first()
            # agency = form.cleaned_data["agency"]
            name = form.cleaned_data["name"]
            status = form.cleaned_data["status"]
            start_date = form.cleaned_data["start_year"]
            end_date = form.cleaned_data["end_year"]
            # given_name = form.cleaned_data[""]
            # surname = request.POST.get("surname")
            noYear = form.cleaned_data["no_year"]

            search_dict = dict()

            if noYear:
                search_dict["no_year"] = noYear
            if type:
                search_dict["award_type"] = type

            if status:
                search_dict["status"] = status

            data = Award.objects.filter(**search_dict)
            # print(data)

            if name:
                data = data.filter(name__icontains=name)
            # if agency:
            #     data = data.filter(agency__name__icontains=agency)
            if start_date:
                data = data.filter(year__gte=start_date)
            if end_date:
                data = data.filter(year__lt=end_date)
            if recipients:
                data = data.filter(recipients__id=recipients.id)
            # if given_name:
            #     data = data.filter(recipients__given_name__icontains=given_name)
            # if surname:
            #     data = data.filter(recipients__surname__icontains=surname)

            return render(request, "test02.html", {"form": form, "n1": data})
        return render(request, "test02.html", {"form": form})
