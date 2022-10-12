from django_tables2 import LazyPaginator
from django_filters.views import FilterView
from django_tables2.export import ExportMixin
from django_tables2.views import SingleTableMixin
from ncard_app import models

from ncard_app.views import tables_class
from ncard_app.views import filters


class FilteredPersonListView(ExportMixin,SingleTableMixin, FilterView):
    filter = None
    table_class = tables_class.PersonTable
    model = models.Person
    template_name = "tables/people.html"
    export_name = "Person"
    filterset_class = filters.PersonFilter
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Person.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredAwardListView(ExportMixin,SingleTableMixin,FilterView):
    filter = None
    table_class = tables_class.AwardTable
    model = models.Award
    template_name = "tables/awards.html"
    filterset_class = filters.AwardFilter
    export_name="Award"
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Award.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredOrganisationListView(SingleTableMixin, FilterView):
    filter = None
    table_class = tables_class.OrganisationTable
    model = models.Organisation
    template_name = "tables/organisations.html"
    filterset_class = filters.OrganisationFilter
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Organisation.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredEventsListView(SingleTableMixin, FilterView):
    filter = None
    table_class = tables_class.EventTable
    model = models.Event
    template_name = "tables/events.html"
    filterset_class = filters.EventFilter
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Event.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredProjectListView(SingleTableMixin, FilterView):
    filter = None
    table_class = tables_class.ProjectTable
    model = models.Project
    template_name = "tables/projects.html"
    filterset_class = filters.ProjectFilter
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Project.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredGrantListView(SingleTableMixin, FilterView):
    filter = None
    table_class = tables_class.GrantTable
    model = models.Grant
    template_name = "tables/grants.html"
    filterset_class = filters.GrantFilter
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Grant.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredPublicationListView(SingleTableMixin, FilterView):
    filter = None
    table_class = tables_class.PublicationTable
    model = models.Publication
    template_name = "tables/publication.html"
    filterset_class = filters.PublicationFilter
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Publication.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs


class FilteredStudentListView(SingleTableMixin, FilterView):
    filter = None
    table_class = tables_class.StudentTable
    model = models.Students
    template_name = "tables/student.html"
    filterset_class = filters.StudentFilter
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = models.Students.objects.all().order_by('id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs
