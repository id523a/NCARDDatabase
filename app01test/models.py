from django.db import models

# Create your models here.
class NcardInfo(models.Model):
    title=models.CharField(max_length= 255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    primary_organisation = models.CharField(max_length=255)
    other_organisation = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Phone = models.CharField(max_length=255)
    NCARD_collaborator = models.CharField(max_length=255)
    Project = models.CharField(max_length=255)
    Twitter_handle = models.CharField(max_length=255)
    Profile_link = models.CharField(max_length=255)


