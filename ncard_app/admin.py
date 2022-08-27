from django.contrib import admin
from ncard_app import models

admin.site.register(models.Person)
admin.site.register(models.Organisation)
admin.site.register(models.Project)
admin.site.register(models.Award)
admin.site.register(models.Event)
admin.site.register(models.Publication)
admin.site.register(models.ContactRecord)
admin.site.register(models.Country)
admin.site.register(models.PersonAddress)
