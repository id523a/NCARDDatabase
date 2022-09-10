from django.views import View
from ncard_app import forms, models
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse


class PhoneBook(View):
    template_name = "predefinedQueries/phone_book.html"

    def get(self, request):
        datalist = models.Organisation.objects.all()
        # print(datalist)
        return render(request, self.template_name, {"data": datalist})

