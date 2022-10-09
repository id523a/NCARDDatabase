from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse
from ncard_app import forms, models

class PersonCreateView(CreateView):
    template_name = 'detail_views/add_person.html'
    form_class = forms.PersonForm
    def get_success_url(self):
        return reverse('list-people')

class PersonUpdateView(UpdateView):
    template_name = 'detail_views/edit_person.html'
    model = models.Person
    form_class = forms.PersonForm
    def get_success_url(self):
        return reverse('list-people')

class OrganisationCreateView(CreateView):
    template_name = 'detail_views/add_organisation.html'
    form_class = forms.OrganisationForm
    def get_success_url(self):
        return reverse('list-organisations')

class OrganisationUpdateView(UpdateView):
    template_name = 'detail_views/edit_organisation.html'
    model = models.Organisation
    form_class = forms.OrganisationForm
    def get_success_url(self):
        return reverse('list-organisations')

class AwardCreateView(CreateView):
    template_name = 'detail_views/add_award.html'
    form_class = forms.AwardForm
    def get_success_url(self):
        return reverse('list-awards')

class AwardUpdateView(UpdateView):
    template_name = 'detail_views/edit_award.html'
    model = models.Award
    form_class = forms.AwardForm
    def get_success_url(self):
        return reverse('list-awards')