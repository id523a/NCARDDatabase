from django.views import View
from django.forms import ModelForm
from django.shortcuts import render, redirect
from ncard_app.models import Person, PersonAddress
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['id', 'surname_first', 'auth_user']
        
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
            ),
            Row('email', css_class='row'),
            Row('email2', css_class='row'),
            Row('phone_office', css_class='row'),
            Row('phone_mobile', css_class='row'),
            Row('phone_home', css_class='row'),
            Row('cre_role', css_class='row'),
            Row('ncard_relation', css_class='row'),
            Row('project', css_class='row'),
            Row('display_on_website', css_class='row'),
            Row('profile_url', css_class='row'),
            Row('orcid_id', css_class='row'),
            Row('scopus_id', css_class='row'),
            Row('wos_researcher_id', css_class='row'),
            Row('google_scholar', css_class='row'),
            Row('researchgate', css_class='row'),
            Row('loop_profile', css_class='row'),
            Row('linkedin', css_class='row'),
            Row('twitter', css_class='row'),
            Row('employers', css_class='row'),
            Row('location', css_class='row'),
            Row('organisation_primary', css_class='row'),
            Row('organisation_other', css_class='row'),
            Row('clinician', css_class='row'),
            Row('notes', css_class='row'),
            Row('research_focus', css_class='row'),
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