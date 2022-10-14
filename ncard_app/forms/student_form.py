from django.forms import ModelForm
from ncard_app import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from crispy_forms.bootstrap import Tab, TabHolder


class StudentForm(ModelForm):
    class Meta:
        model = models.Students
        exclude=["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "student"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout()
