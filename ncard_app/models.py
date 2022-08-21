<<<<<<< HEAD
=======
from django.conf import settings
from django.db import models

class Person(models.Model):
    title = models.CharField(max_length=16, blank=True)
    given_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    surname = models.CharField(max_length=64, blank=True)
    surname_first = models.BooleanField(default=False)
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='person')
    
    @property
    def full_name(self):
        if self.surname_first:
            names = (self.surname, self.given_name, self.middle_name)
        else:
            names = (self.given_name, self.middle_name, self.surname)
        return ' '.join(filter(None, names))
    
    def __str__(self):
        return f'{self.full_name} [{self.id}]'
    
    class Meta:
        verbose_name_plural = 'people'
        ordering = ['surname', 'given_name', 'id']

class ContactRecord(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='contact_record')
    email = models.CharField(max_length=128, blank=True)
    
    def __str__(self):
        return str(self.person)
    
    class Meta:
        ordering = ['person']
>>>>>>> 941c6f6de86aafe3a5c2237391dddab502e8d59f
