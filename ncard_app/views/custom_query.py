from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
import django.db.models.fields as django_fields
from django.db.models import F
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
]

friendly_names = {
    'person.organisations_primary_contact': 'Organisations (by primary contact)',
    'organisation.contacts_primary_org': 'People (by primary org.)',
    'organisation.contacts_other_org': 'People (by other org.)',
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

def get_field_friendly_name(model, field):
    key = f'{model._meta.model_name}.{field.name}'
    if key in friendly_names:
        return friendly_names[key]
    elif hasattr(field, 'verbose_name'):
        verbose_name = field.verbose_name
    else:
        verbose_name = field.name.replace('_', ' ')
    return verbose_name[0].upper() + verbose_name[1:]

extra_fields = {
    models.Person: [
        {'name': 'full_name', 'label': 'Full name', 'type': 'string'},
    ],
}

def schema_entry_model(model):
    fields = []
    # Create list of fields by inspecting model
    for field in model._meta.get_fields():
        field_type = get_field_type(field)
        if field_type != '':
            fields.append({'name': field.name, 'label': get_field_friendly_name(model, field), 'type': field_type})
    # Add any extra computed fields
    fields.extend(extra_fields.get(model, []))
    fields.sort(key=lambda field: field["label"])
    return fields

schema = {model._meta.model_name: schema_entry_model(model) for model in schema_models}

@cache_control(max_age=86400)
@api_login_required
def custom_query_schema(request):
    return JsonResponse(schema)

@login_required
def custom_query(request):
    return render(request, 'custom_query.html')
