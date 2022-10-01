from django.views import View
from django.forms import ModelForm
from django.shortcuts import render, redirect
from ncard_app.models import Person, PersonAddress
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['title', 'given_name', 'middle_name', 'surname']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-1 mb-0'),
                Column('given_name', css_class='col-md-4 mb-0'),
                Column('middle_name', css_class='col-md-3 mb-0'),
                Column('surname', css_class='col-md-4 mb-0'),
                css_class='row'
            )
        )

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