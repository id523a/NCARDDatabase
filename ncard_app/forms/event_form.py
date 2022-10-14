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
            TabHolder(
                Tab('Event Information',
                    HTML("<br>"),
                    Row(
                        Column('title', css_class='col-md-9 mb-0'),
                        Column('event_type', css_class='col-md-3 mb-0'),
                    ),
                    Row(
                        Column('number_attendees', css_class='col-md-3 mb-0'),
                        Column('date', css_class='col-md-3 mb-0'),
                        Column('location', css_class='col-md-6 mb-0'),
                    ),
                    Row(
                        Column(Field('lead_organisation', css_class='selectpicker form-control col-md-3 mb-0', data_live_search='true')),
                        Column(Field('lead_contacts', css_class='selectpicker form-control col-md-9 mb-0', data_live_search='true'))
                    ),
                    Row('detail'),
                ),
                Tab('Participants',
                HTML("<br>"),
                Row('participants'),
                ),
            )
        )