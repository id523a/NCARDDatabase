from pyclbr import Class
from import_export import resources
from ncard_app.models import Organisation, Person, Project, Award, Event, Publication, PersonAddress, Grant, GrantInvestigator, Students

class OrganisationResource(resources.ModelResource):
    class Meta:
        model = Organisation

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project

class AwardResource(resources.ModelResource):
    class Meta:
        model = Award

class EventResource(resources.ModelResource):
    class Meta:
        model = Event

class PublicationResource(resources.ModelResource):
    class Meta:
        model = Publication

class GrantResource(resources.ModelResource):
    class Meta:
        model = Grant    

class studentResource(resources.ModelResource):
    class Meta:
        model = Students