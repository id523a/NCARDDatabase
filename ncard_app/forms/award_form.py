from django.forms import ModelForm
from ncard_app import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from crispy_forms.bootstrap import Tab, TabHolder

class AwardForm(ModelForm):
    class Meta:
        model = models.Award
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "award"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('award_type', css_class='col-md-3 mb-0'),
                Column('name', css_class='col-md-9 mb-0'),
                css_class='row'
            ),
            Row(Field('agency', css_class='selectpicker form-control row', data_live_search='true')),
            Row(
                Column('status', css_class='col-md-2 mb-0'),
                Column(Field('recipients', css_class='selectpicker form-control col-md-10 mb-0', data_live_search='true')),
                css_class='row'
            ),
            Row(
                Column('year', css_class='col-md-2 mb-0'),
                Column('no_year', css_class='col-md-2 mb-0'),
                Column('link', css_class='col-md-8 mb-0'),
                css_class='row'
            ),
            Row('detail', css_class='row'),
            Row('notes', css_class='row'),
        )
