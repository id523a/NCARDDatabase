from django.contrib import admin
from ncard_app import models

admin.site.register(models.Person)
admin.site.register(models.Organisation)
admin.site.register(models.Project)
admin.site.register(models.Award)
admin.site.register(models.Event)
admin.site.register(models.Publication)
admin.site.register(models.Country)
admin.site.register(models.PersonAddress)

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