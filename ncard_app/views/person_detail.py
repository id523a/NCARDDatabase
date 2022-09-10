from django.views import View
from django.forms import ModelForm
from django.shortcuts import render, redirect
from ncard_app.models import Person, ContactRecord, PersonAddress
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['title', 'given_name', 'middle_name', 'surname']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "person"
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

class ContactForm(ModelForm):
    class Meta:
        model = ContactRecord
        fields = [
            "email",
            "email2",
            "phone_office",
            "phone_mobile",
            "phone_home",
            "cre_role",
            "ncard_relation",
            "project",
            "display_on_website",
            "profile_url",
            "orcid_id",
            "scopus_id",
            "wos_researcher_id",
            "google_scholar",
            "researchgate",
            "loop_profile",
            "linkedin",
            "twitter",
            "employers",
            "location",
            "organisation_primary",
            "organisation_other",
            "clinician",
            "notes",
            "research_focus"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "contact"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

class PersonDetail(View):
    def get(self, request, *args, **kwargs):
        person_id = kwargs.get("id", None)
        if person_id is None:
            person_form = PersonForm()
            contact_form = ContactForm()
            return render(request, 'detail_views/add_person.html', {'person_form': person_form, 'contact_form': contact_form})
        else:
            person = Person.objects.get(id=person_id)
            person_form = PersonForm(instance=person)
            try:
                contact = ContactRecord.objects.get(person=person)
                contact_form = ContactForm(instance=contact)
            except ContactRecord.DoesNotExist:
                contact_form = ContactForm()
            return render(request, 'detail_views/edit_person.html', {'id': person_id, 'person_form': person_form, 'contact_form': contact_form})
    
    def post(self, request, *args, **kwargs):
        person_id = kwargs.get("id", None)
        if person_id is None:
            person_form = PersonForm(request.POST)
            contact_form = ContactForm(request.POST)

            if not (person_form.is_valid() and contact_form.is_valid()):
                return render(request, 'detail_views/add_person.html', {'person_form': person_form, 'contact_form': contact_form})

            person_instance = person_form.save()
            contact_instance = contact_form.save(commit=False)
            contact_instance.person = person_instance
            contact_instance.save()
            contact_form.save_m2m()
        else:
            person = Person.objects.get(id=person_id)
            contact, _ = ContactRecord.objects.get_or_create(person=person)
            
            person_form = PersonForm(request.POST, instance=person)
            contact_form = ContactForm(request.POST, instance=contact)
            
            if not (person_form.is_valid() and contact_form.is_valid()):
                return render(request, 'detail_views/edit_person.html', {'id': person_id, 'person_form': person_form, 'contact_form': contact_form})
            
            person_form.save()
            contact_form.save()
        return redirect('list-people')