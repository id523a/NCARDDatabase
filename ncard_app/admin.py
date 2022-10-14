from django.contrib import admin
from ncard_app import models
from import_export.admin import ImportExportModelAdmin

class PersonAdmin(ImportExportModelAdmin):
    pass
admin.site.register(models.Person, PersonAdmin)

class ProjectAdmin(ImportExportModelAdmin):
    pass
admin.site.register(models.Project, ProjectAdmin)

class AwardAdmin(ImportExportModelAdmin):
    pass
admin.site.register(models.Award, AwardAdmin)

class EventAdmin(ImportExportModelAdmin):
    pass
admin.site.register(models.Event, EventAdmin)

class PublicationAdmin(ImportExportModelAdmin):
    pass
admin.site.register(models.Publication, PublicationAdmin)

admin.site.register(models.Country)
admin.site.register(models.Students)

class GrantInvestigatorInline(admin.TabularInline):
    model = models.GrantInvestigator
    fields = ['investigator', 'chief']
    extra = 1

class GrantAdmin(admin.ModelAdmin):
    inlines = [
        GrantInvestigatorInline
    ]
    exclude = ['investigators']

admin.site.register(models.Grant, GrantAdmin)

class OrganisationAdmin(ImportExportModelAdmin):
    list_display = ("name","primary_contact","phone","website","twitter_handle","organisation_type")
    pass

admin.site.register(models.Organisation, OrganisationAdmin)

