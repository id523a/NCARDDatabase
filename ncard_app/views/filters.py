from django.db.models import Q

from ncard_app import models
import django_filters


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
                                      label="name")

    class Meta:
        model = models.Award
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Award.objects.all().filter(

            Q(name__icontains=value)

        )


class OrganisationFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="name")

    class Meta:
        model = models.Organisation
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Organisation.objects.all().filter(

            Q(name__icontains=value)

        )


class EventFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="title")

    class Meta:
        model = models.Event
        fields = {
            # 'given_name':['icontains',]
        }

    def universal_search(self, queryset, name, value):
        return models.Event.objects.all().filter(

            Q(title__icontains=value)

        )


class ProjectFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="name")

    class Meta:
        model = models.Project
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Project.objects.all().filter(

            Q(name__icontains=value)

        )


class GrantFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="title")

    class Meta:
        model = models.Grant
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Grant.objects.all().filter(

            Q(title__icontains=value)

        )


class PublicationFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="title")

    class Meta:
        model = models.Publication
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Publication.objects.all().filter(

            Q(title__icontains=value)

        )


class StudentFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="name")

    class Meta:
        model = models.Students
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Students.objects.all().filter(

            Q(name__icontains=value)

        )
