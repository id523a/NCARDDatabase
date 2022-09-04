from django.forms import ModelForm
from ncard_app import models
from django import forms


class AwardForm(ModelForm):
    # award_type = forms.CharField(label="Type",widget=,required=False)
    start_year = forms.IntegerField(
        label="startDate",

        required=False
    )
    # end_year = forms.DateField(
    #     label="endDate",
    #     widget=forms.DateInput(attrs={"type": "text"}),
    #     required=False
    # )
    end_year = forms.IntegerField(
        label="endDate",

        required=False
    )

    class Meta:
        model = models.Award
        # fields = ["award_type", "agency", "name", "recipients", "status", "", "noYear", "", ""]
        exclude = ["detail", "year", "notes", "link", "agency"]
        # widgets = {
        #     "award_type": forms.TextInput(attrs={"class": "input-group"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        for name, field in self.fields.items():

            field.widget.attrs = {"class": "input-group", "placeholder": field.label}

    def SetAllRequired(self):
        for field in self.fields:
            self.fields[field].required = False
            # self.form.fields[field].help_text = "非必填"
