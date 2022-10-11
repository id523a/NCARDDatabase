from django.forms import ModelForm
from ncard_app import models
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from crispy_forms.bootstrap import Tab, TabHolder


class EventForm(ModelForm):
    date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    class Meta:
        model = models.Event
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "event"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('event_type', css_class='col-md-3 mb-0'),
                Column('date', css_class='col-md-5 mb-0'),
                Column('number_attendees', css_class='col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('title', css_class='col-md-2 mb-0'),
                Column('location', css_class='col-md-10 mb-0'),
                css_class='row'
            ),
            Row(Field('lead_organisation', css_class='selectpicker form-control row', data_live_search='true')),
            Row(Field('lead_contacts', css_class='selectpicker form-control row', data_live_search='true')),
            Row('detail', css_class='row'),
            Row('participants', css_class='row'),

        )