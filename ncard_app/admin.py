from django.contrib import admin
from ncard_app import models

admin.site.register(models.Person)
admin.site.register(models.ContactRecord)