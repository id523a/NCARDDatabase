from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django_tables2 import LazyPaginator
from django_tables2.utils import A

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
    start_date = request.POST.get("startDate")
    end_date = request.POST.get("endDate")
    given_name = request.POST.get("givenName")
    surname = request.POST.get("surname")
    noYear = request.POST.get("noYear")

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
        data = data.filter(name__icontains=name)
    if agency:
        data = data.filter(agency__name__icontains=agency)
    if start_date:
        data = data.filter(year__gte=start_date)
    if end_date:
        data = data.filter(year__lt=end_date)

    if given_name:
        data = data.filter(recipients__given_name__icontains=given_name)
    if surname:
        data = data.filter(recipients__surname__icontains=surname)

    return render(request, "test01.html", {"n1": data})


import django_tables2 as tables


class PersonTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), )

    class Meta:
        model = models.Person
        # fields=('given_name','title')
        exclude = ('id', 'surname_first', 'auth_user')
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-person", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

import django_filters


class PersonFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label="title, given name, first name, primary organisation")

    class Meta:
        model = models.Person
        fields = {
            # 'given_name':['icontains',]
        }

    def universal_search(self, queryset, name, value):
        return models.Person.objects.all().filter(
<<<<<<< HEAD
            Q(phone_home__icontains=value) | Q(given_name__icontains=value) | Q(title__icontains=value) | Q(organisation_primary__name__icontains=value)
=======
            Q(surname__icontains=value) | Q(given_name__icontains=value) | Q(title__icontains=value) | Q(organisation_primary__name__icontains=value)
>>>>>>> 680c8c4caaf8060aeddfeab01247620e9613a663
        )


class FilteredPersonListView(SingleTableMixin, FilterView):
    filter = None
    table_class = PersonTable
    model = models.Person
    template_name = "searchBar/person_list.html"
    filterset_class = PersonFilter
    paginator_class = LazyPaginator
    paginate_by = 10


    def get_queryset(self, **kwargs):
        qs = models.Person.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs
