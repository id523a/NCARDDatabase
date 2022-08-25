from django.contrib import admin
from ncard_app import models

admin.site.register(models.Person)
admin.site.register(models.Organisation)
admin.site.register(models.ContactRecord)
admin.site.register(models.PersonAddress)
admin.site.register(models.Project)
