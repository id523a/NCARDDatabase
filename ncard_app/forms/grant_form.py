from django.forms import ModelForm
from ncard_app import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from crispy_forms.bootstrap import Tab, TabHolder

class GrantForm(ModelForm):
    class Meta:
        model = models.Grant
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "grant"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row('title'),
            Row('reference'),
            Row('project'),
            Row(Field('investigators', css_class='selectpicker form-control row mb-0', data_live_search='true')),
        )