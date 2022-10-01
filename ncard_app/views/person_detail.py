from django.views import View
from django.shortcuts import render, redirect
from ncard_app.models import Person, PersonAddress
from ncard_app.forms import PersonForm

class PersonDetail(View):
    def get(self, request, *args, **kwargs):
        person_id = kwargs.get("id", None)
        if person_id is None:
            person_form = PersonForm()
            return render(request, 'detail_views/add_person.html', {'person_form': person_form })
        else:
            person = Person.objects.get(id=person_id)
            person_form = PersonForm(instance=person)
            return render(request, 'detail_views/edit_person.html', {'id': person_id, 'person_form': person_form })
    
    def post(self, request, *args, **kwargs):
        person_id = kwargs.get("id", None)
        if person_id is None:
            person_form = PersonForm(request.POST)
            if not person_form.is_valid():
                return render(request, 'detail_views/add_person.html', {'person_form': person_form })

            person_instance = person_form.save()
        else:
            person = Person.objects.get(id=person_id)
            person_form = PersonForm(request.POST, instance=person)
            if not person_form.is_valid():
                return render(request, 'detail_views/edit_person.html', {'id': person_id, 'person_form': person_form })
            
            person_form.save()
        return redirect('list-people')