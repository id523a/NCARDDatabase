from django.forms import ModelForm
from ncard_app import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from crispy_forms.bootstrap import Tab, TabHolder

class OrganisationForm(ModelForm):
    class Meta:
        model = models.Organisation
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "organisation"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-9 mb-0'),
                Column('organisation_type', css_class='col-md-3 mb-0'),
            ),
            Row(Field('primary_contact', css_class='selectpicker form-control row mb-0', data_live_search='true')),
            Row(
                Column('phone', css_class='col-md-3 mb-0'),
                Column('website', css_class='col-md-6 mb-0'),
                Column('twitter_handle', css_class='col-md-3 mb-0'),
             ),
        )