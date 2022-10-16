from import_export import resources
from import_export.widgets import ForeignKeyWidget

from ncard_app.models import (Award, Event, Grant, Organisation, Person,
                              Project, Publication, Students)


class OrganisationResource(resources.ModelResource):
    class Meta:
        model = Organisation

class PersonResource(resources.ModelResource):
    organisation_primary = fields.field(column_name='organisation_primary', attribute='organisation_primary', widget=ForeignKeyWidget(Organisation,'name'))
    organisation_other = fields.field(column_name='organisation_primary', attribute='organisation_primary', widget=ForeignKeyWidget(Organisation,'name'))
    class Meta:
        model = Person

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project

class AwardResource(resources.ModelResource):
    class Meta:
        model = Award

class EventResource(resources.ModelResource):
    lead_organisation = fields.field(column_name='lead_organisation', attribute='lead_organisation', widget=ForeignKeyWidget(Organisation,'name'))
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