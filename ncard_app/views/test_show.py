from django.shortcuts import render, redirect
from ncard_app.models import Award
from django.contrib import messages
from ncard_app import models

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


import django_tables2 as tables


class PersonTable(tables.Table):
    class Meta:
        model = models.Person
        # fields=('given_name',)
        attrs = {"class": "table table-striped"}



from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

# views.py
def person_list(request):
    table = PersonTable(models.Person.objects.all())

    return render(request, "searchBar/person_list.html", {
        "table": table
    })

import django_filters
class PersonFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    given_name= django_filters.CharFilter(lookup_expr='icontains',label="given_name")
    class Meta:
        model = models.Person
        fields = {
            # 'given_name':['icontains',]
                  }

class FilteredPersonListView(SingleTableMixin, FilterView):
    filter=None
    table_class = PersonTable
    model = models.Person
    template_name = "searchBar/person_list.html"
    filterset_class = PersonFilter

    def get_queryset(self, **kwargs):
        qs = models.Person.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs
