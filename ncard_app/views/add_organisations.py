from django.views import View
from ncard_app import forms, models
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib import messages


class OrganisationAdd(View):
    template_name = "detail_views/add_organisation.html"

    def get(self, request):
        form = forms.OrganisationForm()

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = forms.OrganisationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(reverse("list-organisations"))

        return render(request, self.template_name, {"form": form})
