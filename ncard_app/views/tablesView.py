from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django_tables2 import LazyPaginator
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from ncard_app import models
import django_filters
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


class AwardTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), )

    class Meta:
        model = models.Award
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-award", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')

class OrganisationTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), )

    class Meta:
        model = models.Organisation
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-organisation", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')

class EventTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), )

    class Meta:
        model = models.Event
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-events", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


class PersonFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="title, given name, first name, primary organisation")

    class Meta:
        model = models.Person
        fields = {
            # 'given_name':['icontains',]
        }

    def universal_search(self, queryset, name, value):
        return models.Person.objects.all().filter(

            Q(surname__icontains=value) | Q(given_name__icontains=value) | Q(title__icontains=value) | Q(
                organisation_primary__name__icontains=value) | Q(project__icontains=value)

        )


class AwardFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")

    class Meta:
        model = models.Award
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Award.objects.all().filter(

            Q(name__icontains=value)

        )

class OrganisationFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")

    class Meta:
        model = models.Organisation
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Organisation.objects.all().filter(

            Q(name__icontains=value)

        )

class EventFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="title, given name, first name, primary organisation")

    class Meta:
        model = models.Event
        fields = {
            # 'given_name':['icontains',]
        }

    def universal_search(self, queryset, name, value):
        return models.Event.objects.all().filter(

            Q(title__icontains=value)

        )


class FilteredPersonListView(SingleTableMixin, FilterView):
    filter = None
    table_class = PersonTable
    model = models.Person
    template_name = "tables/people.html"
    filterset_class = PersonFilter
    paginator_class = LazyPaginator
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Person.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredAwardListView(SingleTableMixin, FilterView):
    filter = None
    table_class = AwardTable
    model = models.Award
    template_name = "tables/awards.html"
    filterset_class = AwardFilter
    paginator_class = LazyPaginator
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Award.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredOrganisationListView(SingleTableMixin, FilterView):
    filter = None
    table_class = OrganisationTable
    model = models.Organisation
    template_name = "tables/organisations.html"
    filterset_class = OrganisationFilter
    paginator_class = LazyPaginator
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Organisation.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

class FilteredEventsListView(SingleTableMixin, FilterView):
    filter = None
    table_class = EventTable
    model = models.Event
    template_name = "tables/events.html"
    filterset_class = EventFilter
    paginator_class = LazyPaginator
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Event.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs