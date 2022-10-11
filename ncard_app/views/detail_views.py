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


class EventCreateView(CreateView):
    template_name = 'detail_views/add_event.html'
    form_class = forms.EventForm

    def get_success_url(self):
        return reverse('list-events')


class EventUpdateView(UpdateView):
    template_name = 'detail_views/edit_event.html'
    model = models.Event
    form_class = forms.EventForm

    def get_success_url(self):
        return reverse('list-events')


class ProjectCreateView(CreateView):
    template_name = 'detail_views/add_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('list-projects')


class ProjectUpdateView(UpdateView):
    template_name = 'detail_views/edit_project.html'
    model = models.Project
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('list-projects')


class GrantCreateView(CreateView):
    template_name = 'detail_views/add_grant.html'
    form_class = forms.GrantForm

    def get_success_url(self):
        return reverse('list-grants')


class GrantUpdateView(UpdateView):
    template_name = 'detail_views/edit_grant.html'
    model = models.Grant
    form_class = forms.GrantForm

    def get_success_url(self):
        return reverse('list-grants')


class PublicationCreateView(CreateView):
    template_name = 'detail_views/add_publication.html'
    form_class = forms.PublicationForm

    def get_success_url(self):
        return reverse('list-publications')


class PublicationUpdateView(UpdateView):
    template_name = 'detail_views/edit_publication.html'
    model = models.Publication
    form_class = forms.PublicationForm

    def get_success_url(self):
        return reverse('list-publications')


class StudentCreateView(CreateView):
    template_name = 'detail_views/add_student.html'
    form_class = forms.StudentForm

    def get_success_url(self):
        return reverse('list-students')


class StudentUpdateView(UpdateView):
    template_name = 'detail_views/edit_student.html'
    model = models.Students
    form_class = forms.StudentForm

    def get_success_url(self):
        return reverse('list-students')
