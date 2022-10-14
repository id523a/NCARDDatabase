from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
import django.db.models.fields as django_fields
from django.db.models import F, Q
from django.core.exceptions import SuspiciousOperation

import json

from ncard_app import models
from .decorators import login_required, api_login_required

schema_models = [
    models.Organisation,
    models.Person,
    models.Project,
    models.Award,
    models.Event,
    models.Publication,
    models.Country,
    models.PersonAddress,
    models.Grant,
    models.Students,
]

friendly_names = {
    'person.organisations_primary_contact': 'Organisations (by primary contact)',
    'organisation.contacts_primary_org': 'People (by primary org.)',
    'organisation.contacts_other_org': 'People (by other org.)',
    'person.student_info': 'Student info',
    'person.students_supervising': 'Students supervising',
    'award.scholarship_recipient': 'Scholarship recipient',
}

field_type_map = {
    django_fields.BooleanField: 'boolean',
    django_fields.IntegerField: 'integer',
    django_fields.BigIntegerField: 'integer',
    django_fields.PositiveSmallIntegerField: 'integer',
    django_fields.PositiveIntegerField: 'integer',
    django_fields.DecimalField: 'decimal',
    django_fields.DateField: 'date',
}

def get_field_type(field):
    if field.related_model is not None:
        return field.related_model._meta.model_name
    elif field.auto_created:
        return ''
    elif field.choices is not None:
        return field.choices
    elif isinstance(field, django_fields.CharField):
        return 'string'
    else:
        return field_type_map.get(type(field), '')

def capitalize_first(name):
    return name[0].upper() + name[1:]

def get_field_friendly_name(model, field):
    key = f'{model._meta.model_name}.{field.name}'
    if key in friendly_names:
        return friendly_names[key]
    elif hasattr(field, 'verbose_name'):
        verbose_name = field.verbose_name
    else:
        verbose_name = field.name.replace('_', ' ')
    return capitalize_first(verbose_name)

"""
extra_fields = {
    models.Person: [
        {'name': 'full_name', 'label': 'Full name', 'type': 'string'},
    ],
}
"""

iso_week_day_type = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]

schema_enums = [
    iso_week_day_type
]

def get_schema_meta(model):
    return {
        'singular': capitalize_first(model._meta.verbose_name),
        'plural': capitalize_first(model._meta.verbose_name_plural)
    }

schema_meta = {model._meta.model_name: get_schema_meta(model) for model in schema_models}

schema_meta['date'] = {'fakeTable': True, 'singular': 'Date', 'plural': 'Dates'}

def get_schema_fields(model):
    # Add computed fields first
    # fields = list(extra_fields.get(model, []))
    fields = {}
    # Create list of fields by inspecting model
    for field in model._meta.get_fields():
        field_type = get_field_type(field)
        if not isinstance(field_type, str):
            enum_index = len(schema_enums)
            schema_enums.append(field_type)
            field_type = f'enum{enum_index}'
        if field_type != '':
            fields[field.name] = {'label': get_field_friendly_name(model, field), 'type': field_type}
    return fields

schema_fields = {model._meta.model_name: get_schema_fields(model) for model in schema_models}

schema_fields['date'] = {
    'year': {'label': 'Year', 'type': 'integer'},
    'month': {'label': 'Month', 'type': 'integer'},
    'day': {'label': 'Day of month', 'type': 'integer'},
    'week': {'label': 'Week of year', 'type': 'integer'},
    'iso_week_day': {'label': 'Day of week', 'type': 'enum0'}
}

schema = {
    'enums': schema_enums,
    'meta': schema_meta,
    'fields': schema_fields
}

@cache_control(max_age=86400)
@api_login_required
def custom_query_schema(request):
    return JsonResponse(schema)

@login_required
def custom_query(request):
    return render(request, 'custom_query.html')

@api_login_required
def custom_query_data(request):
    if not request.method == 'POST':
        raise SuspiciousOperation("Must use POST request.")
    if len(request.body) > 16384:
        raise SuspiciousOperation("Query is too long.")
    body = json.loads(request.body)
    
    # Get starting model from table name
    start_table = body["startTable"]
    if not isinstance(start_table, str):
        raise SuspiciousOperation("Invalid starting table.")

    start_model = None
    for model in schema_models:
        if model._meta.model_name == start_table:
            start_model = model
            break
    
    if start_model is None:
        raise SuspiciousOperation("Invalid starting table.")
    
    objs = start_model.objects.all()
    
    # Validate field selection
    try:
        fields_cleaned = []
        for subfield_list in body["fields"]:
            current_type = start_table
            subfields_cleaned = []
            for subfield in subfield_list:
                subfield_info = schema_fields[current_type][subfield]
                current_type = subfield_info['type']
                subfields_cleaned.append(subfield)
            if current_type in schema_meta and not schema_meta[current_type].get('fakeTable', False):
                subfields_cleaned.append('id')
            fields_cleaned.append("__".join(subfields_cleaned))
    except TypeError:
        raise SuspiciousOperation("Invalid field selection.")
    except KeyError:
        raise SuspiciousOperation("Invalid field selection.")
    # TODO: Support computed fields such as full_name
    
    # TODO: Filter the rows

    return JsonResponse(list(objs.values_list(*fields_cleaned)), safe=False)