from django import forms
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import JsonResponse
from django.views import View
from crispy_forms.helper import FormHelper
from django.apps import apps
from ncard_app import models, serializer
import json
from django.shortcuts import render


class AwardForm(ModelForm):
    # award_type = forms.CharField(label="Type",widget=,required=False)

    start_year = forms.IntegerField(
        label="startDate",

        required=False,
        widget=forms.TextInput(attrs={"Date-class": "year_select"}),
    )
    # end_year = forms.DateField(
    #     label="endDate",
    #     widget=forms.DateInput(attrs={"type": "text"}),
    #     required=False
    # )
    end_year = forms.IntegerField(
        label="endDate",
        widget=forms.TextInput(attrs={"Date-class": "year_select"}),
        required=False,
    )
    recipients = forms.ModelChoiceField(
        queryset=models.Person.objects.all(),
        empty_label="---------------",
        widget=forms.Select(attrs={"class":"selectpicker","data-live-search":"true"}),
    )

    class Meta:
        model = models.Award
        # fields = ["award_type", "agency", "name", "recipients", "status", "", "noYear", "", ""]
        exclude = ["detail", "year", "notes", "link"]
        # widgets = {
        #     "award_type": forms.TextInput(attrs={"class": "input-group"})
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "input-group", "placeholder": field.label}

    def SetAllRequired(self):
        for field in self.fields:
            self.fields[field].required = False
            # self.form.fields[field].help_text = "非必填"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "award"
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        # self.helper.use_custom_control = False
        # self.helper.layout = Layout(
        #     Field('type', css_class='year_select')
        # )


class OrganisationForm(ModelForm):
    class Meta:
        model = models.Organisation
        # fields = "__all__"
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "organisation"
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # self.helper.disable_csrf = True


class PersonForm(ModelForm):
    class Meta:
        model = models.Person
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "person"
        self.helper = FormHelper(self)
        self.helper.form_tag = False

class QuerySearch(View):

    def get(self, request):
        models_list = list(apps.get_app_config('app01test').get_models())
        table_fields = {}

        for model in models_list:
            table_name = model._meta.db_table.split("_")[1]

            table_fields[table_name] = []
            for fields in model._meta.fields:
                if fields.name == "id":
                    continue
                table_fields[table_name].append(fields.name)

        form = dict()
        form['award'] = AwardForm().as_div()
        form['person'] = PersonForm().as_div()
        form['organisation'] = OrganisationForm().as_div()
        data = json.dumps(form)
        return render(request, "querySearch/search.html",
                      {"table_list": table_fields, "form": data, "table_list_json": json.dumps(table_fields)})

    def post(self, request):
        query_dic = {}

        data = request.POST

        self.parse_query_condition(data, query_dic)

        result_query = None
        for key, value in query_dic.items():
            fun = getattr(self, key)
            result_query = fun(value, result_query)

        award_ser = serializer.AwardSerializer(instance=result_query, many=True)
        print(award_ser.data)

        return JsonResponse({"result_set": award_ser.data})

    @staticmethod
    def parse_query_condition(data: dict, query_dic):
        for key in data.keys():
            if key == 'csrfmiddlewaretoken':
                continue

            val_list = key.split('-')

            table_name = val_list[0]
            filed = val_list[len(val_list) - 1]

            if table_name not in query_dic:
                query_dic[table_name] = {}
            if filed not in query_dic[table_name]:
                query_dic[table_name][filed] = []
            for client_input in data.getlist(key):
                query_dic[table_name][filed].append(client_input)

    def award(self, data: dict, result_query):
        # award=models.Award.objects.all().select_related('agency')
        # award2=models.Award.objects.all().prefetch_related('recipients').all()
        if result_query is None:
            award = models.Award.objects.all().select_related('agency').prefetch_related('recipients')
        else:
            award = result_query

        dict_award = {
            'award_type': self.award_type,
            'name': self.award_name,
            'start_year': self.award_start_year,

        }
        for key, values in data.items():
            method = dict_award.get(key, None)
            if method:
                result = models.Award.objects.none()
                for value in values:
                    result = method(value, award, result)
                if result.exists():
                    award = result

        return award

    def person(self, data: dict, result_query):
        if result_query is None:
            person = models.Award.objects.all().select_related('agency').prefetch_related('recipients')
        else:
            person = result_query

        dict_person = {
            'title': self.person_title,

        }

        for key, values in data.items():
            method = dict_person.get(key, None)
            if method:
                result = models.Award.objects.none()
                for value in values:
                    if value == '':
                        continue
                    result = method(value, person, result)

                if result.exists():
                    person = result

        return person

    @staticmethod
    def award_type(value, queryset: QuerySet[models.Award], result):
        result |= queryset.filter(award_type=value)
        return result

    @staticmethod
    def award_name(value, queryset: QuerySet[models.Award], result):
        result |= queryset.filter(name__icontains=value)
        return result

    @staticmethod
    def award_start_year(value, queryset: QuerySet[models.Award], result):
        result |= queryset.filter(year__gte=value)
        return result

    @staticmethod
    def award_end_year(value, queryset: QuerySet[models.Award], result):
        result |= queryset.filter(year__lt=value)
        return result

    @staticmethod
    def person_title(value, queryset: QuerySet[models.Person], result):
        result |= queryset.filter(recipients__title__icontains=value)
        return result
