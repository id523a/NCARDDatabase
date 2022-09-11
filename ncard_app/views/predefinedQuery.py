import csv
import json

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


def export(request):
    datalist = json.loads(request.POST.get('datalist'))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="organisation.csv"'
    writer = csv.writer(response)
    for row in datalist:
        writer.writerow(row)
    return response
