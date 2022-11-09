from django.db.models import Q

from ncard_app import models
import django_filters


class PersonFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="title, first & last name, primary organisation, project")

    class Meta:
        model = models.Person
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Person.objects.all().filter(

            Q(surname__icontains=value) | Q(given_name__icontains=value) | Q(title__icontains=value) | Q(
                organisation_primary__name__icontains=value) | Q(project__icontains=value)

        )


class AwardFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="award name, type, agency, year")

    class Meta:
        model = models.Award
        fields = {}

    def universal_search(self, queryset, name, value):
        qs = Q(name__icontains=value) | Q(agency__name__icontains=value) | Q(year__icontains=value)

        for index, choice_name in models.Award.AwardType.choices:
            if value.lower() in choice_name.lower():
                qs.add(Q(award_type=index), Q.OR)
            
        return models.Award.objects.all().filter(qs)


class OrganisationFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="name, type")

    class Meta:
        model = models.Organisation
        fields = {}

    def universal_search(self, queryset, name, value):
        qs = Q(name__icontains=value)

        for index, choice_name in models.Organisation.OrganisationType.choices:
            if value.lower() in choice_name.lower():
                qs.add(Q(organisation_type=index), Q.OR)

        return models.Organisation.objects.all().filter(qs)


class EventFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="type, event title")

    class Meta:
        model = models.Event
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Event.objects.all().filter(

            Q(title__icontains=value) | Q(event_type__icontains=value) 

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
                                      label="reference, title, project")

    class Meta:
        model = models.Grant
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Grant.objects.all().filter(

            Q(reference__icontains=value) | Q(title__icontains=value) | Q(project__name__icontains=value)

        )


class PublicationFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="title, type, year, journal, doi")

    class Meta:
        model = models.Publication
        fields = {}

    def universal_search(self, queryset, name, value):
        return models.Publication.objects.all().filter(

            Q(publication_type=value) | Q(year__icontains=value) | Q(title__icontains=value) | Q(journal__icontains=value) | Q(doi__icontains=value) 

        )


class StudentFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="name, type, title topic")

    class Meta:
        model = models.Students
        fields = {}

    def universal_search(self, queryset, name, value):
        qs = Q(student_name__given_name__icontains=value) | Q(student_name__surname__icontains=value) | Q(title_topic__icontains=value) 

        for index, choice_name in models.Students.StudentTypes.choices:
            if value.lower() in choice_name.lower():
                qs.add(Q(student_type=index), Q.OR)
    
        return models.Students.objects.all().filter(qs)
