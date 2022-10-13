from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from ncard_app import models
import django_tables2 as tables


def get_formats():
    formats = ['csv']
    return formats


class PersonTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

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
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

    class Meta:
        model = models.Award
        exclude = ('id', 'notes', 'detail',)
        attrs = {"class": "table table-striped", "th": {"scope": "col", "id": "award-table"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-award", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


class OrganisationTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

    class Meta:
        model = models.Organisation
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col", "id": "award-table"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-organisation", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


class EventTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

    class Meta:
        model = models.Event
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-event", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


class ProjectTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

    class Meta:
        model = models.Project
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-project", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


class GrantTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

    class Meta:
        model = models.Grant
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-grant", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


class PublicationTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

    class Meta:
        model = models.Publication
        exclude = ('id',)
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-publication", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')


class StudentTable(tables.Table):
    edit = tables.Column('Action',
                         orderable=False, empty_values=(), exclude_from_export=True)
    export_formats = get_formats()

    class Meta:
        model = models.Students
        attrs = {"class": "table table-striped", "th": {"scope": "col"}}

    def render_edit(self, record):
        return mark_safe(
            '<a href=' + reverse_lazy("edit-student", args=[record.pk]) + ' class="btn btn-sm ncard_btn">Edit</a>')
