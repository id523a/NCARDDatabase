from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from ncard_app import models
from ncard_app.views.resources import EventResource

admin.site.register(models.Country)

class GrantInvestigatorInline(admin.TabularInline):
    model = models.GrantInvestigator
    fields = ['investigator', 'chief']
    extra = 1

class GrantAdmin(ImportExportModelAdmin):
    list_display = ("title", "reference", "project")
    inlines = [
        GrantInvestigatorInline
    ]
    exclude = ['investigators']

admin.site.register(models.Grant, GrantAdmin)

class OrganisationAdmin(ImportExportModelAdmin):
    list_display = ("name","primary_contact","phone","website","twitter_handle","organisation_type")
    pass
admin.site.register(models.Organisation, OrganisationAdmin)

class EventAdmin(ImportExportModelAdmin):
    list_display = ("event_type", "date", "number_attendees", "title", "detail", "lead_organisation", "location")
    resources_class = EventResource
    pass
admin.site.register(models.Event, EventAdmin)

class PublicationAdmin(ImportExportModelAdmin):
    list_display = ("title","publication_type","ncard_publication","year","journal","journal_ISSN","volume","page_start","page_end","open_access_status","doi","electronic_ISBN","print_ISBN","abstract","citation","source_ID")
    pass
admin.site.register(models.Publication, PublicationAdmin)

class StudentsAdmin(ImportExportModelAdmin):
    list_displays = ('student_name','student_type','supervisor','title_topic','year_start','year_end','scholarship')
    pass
    
admin.site.register(models.Students, StudentsAdmin)

class AwardAdmin(ImportExportModelAdmin):
    list_displays = ('name', 'award_type', 'agency', 'recipients', 'status', 'detail', 'year', 'no_year', 'notes', 'link')
    pass
admin.site.register(models.Award, AwardAdmin)

class ProjectAdmin(ImportExportModelAdmin):
    list_displays = ('name','lead','status','funded')
    pass
admin.site.register(models.Project, ProjectAdmin)

class PersonAdmin(ImportExportModelAdmin):
    list_displays = ('title','given_name','middle_name','surname','surname_first','email','email2','phone_office','phone_mobile','phone_home','cre_role','ncard_relation','project','display_on_website','profile_url','orcid_id','scopus_id','wos_researcher_id','google_scholar','researchgate','loop_profile','linkedin','twitter','location','organisation_primary','organisation_other','clinician','research_focus','work_line1','work_line2','work_line3','work_suburb','work_state','work_postcode','work_country','home_line1','home_line2','home_line3','home_suburb','home_state', 'home_postcode', 'home_country', 'notes')
admin.site.register(models.Person, PersonAdmin)