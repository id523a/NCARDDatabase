from django.forms import ModelForm
from ncard_app import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML
from crispy_forms.bootstrap import Tab, TabHolder

class PersonForm(ModelForm):
    class Meta:
        model = models.Person
        fields = '__all__'
        exclude = ['id', 'surname_first', 'auth_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "person"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab('Contact Details',
                    HTML("<br>"),
                    Row(
                        Column('title', css_class='col-md-1 mb-0'),
                        Column('given_name', css_class='col-md-4 mb-0'),
                        Column('middle_name', css_class='col-md-3 mb-0'),
                        Column('surname', css_class='col-md-4 mb-0'),
                    ),
                    Row(
                        Column('email'),
                        Column('email2'),
                    ),
                    Row(
                        Column('phone_office'),
                        Column('phone_mobile'),
                        Column('phone_home'),
                    ),
                ),
                
                Tab('NCARD Info',
                    HTML("<br>"),
                    Row(
                        Column('cre_role', css_class='col-md-4 mb-0'),
                        Column('ncard_relation', css_class='col-md-4 mb-0'),
                        Column('project', css_class='col-md-4 mb-0'),
                    ),
                    Row(
                        Column('display_on_website', css_class='col-md-3 mb-0'),
                        Column('profile_url', css_class='col-md-9 mb-0'),
                    ),
                ),

                Tab('Researcher Profile',
                    HTML("<br>"),
                    Row(
                        Column('clinician', css_class='col-md-2 mb-0'),
                        Column('research_focus', css_class='col-md-10 mb-0'),
                    ),
                    Row(
                        Column('orcid_id', css_class='col-md-4 mb-0'),
                        Column('scopus_id', css_class='col-md-4 mb-0'),
                        Column('wos_researcher_id', css_class='col-md-4 mb-0'),
                    ),
                    Row('google_scholar'),
                    Row('researchgate'),
                    Row('loop_profile'),
                    Row(
                        Column('linkedin', css_class='col-md-5 mb-0'),
                        Column('twitter', css_class='col-md-3 mb-0'),
                    ),
                ),

                Tab('Organisational Info',
                    HTML("<br>"),
                    Row(Field('employers', css_class='selectpicker form-control', data_live_search='true')),
                    Row('location'),
                    Row('organisation_primary'),
                    Row('organisation_other'),
                ),

                Tab('Notes',
                    HTML("<br>"),
                    Row('notes'),
                ),
            )
        )


