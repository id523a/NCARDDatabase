from django.forms import ModelForm
from ncard_app import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from crispy_forms.bootstrap import Tab, TabHolder


class StudentForm(ModelForm):
    class Meta:
        model = models.Students
        exclude=["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "student"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML("<br>"),
            Row(
                Column(Field('student_name', css_class='selectpicker form-control col-md-9 mb-0', data_live_search='true')),
                Column('student_type', css_class='col-md-3 mb-0'),
            ),            
            Row(Field('supervisor', css_class='selectpicker form-control row', data_live_search='true')),
            Row('title_topic'),
            Row(
                Column('year_start', css_class='col-md-2 mb-0'),
                Column('year_end', css_class='col-md-2 mb-0'),
                Column(Field('scholarship', css_class='selectpicker form-control col-md-8 mb-0', data_live_search='true')),
            ),
        )