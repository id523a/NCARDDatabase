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

def get_schema_meta(model):
    return {
        'singular': capitalize_first(model._meta.verbose_name),
        'plural': capitalize_first(model._meta.verbose_name_plural)
    }

schema_meta = {model._meta.model_name: get_schema_meta(model) for model in schema_models}

schema_meta['date'] = {'fakeTable': True, 'singular': 'Date', 'plural': 'Dates'}

def get_schema_fields(model):
    fields = {}
    # Create list of fields by inspecting model
    for field in model._meta.get_fields():
        field_type = get_field_type(field)
        enum_choices = None
        if not isinstance(field_type, str):
            enum_choices = field_type
            field_type = 'enum'
        if field_type != '':
            fields[field.name] = {'label': get_field_friendly_name(model, field), 'type': field_type}
        if enum_choices is not None:
            fields[field.name]['choices'] = enum_choices
    return fields

schema_fields = {model._meta.model_name: get_schema_fields(model) for model in schema_models}

iso_week_day_choices = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]

schema_fields['date'] = {
    'year': {'label': 'Year', 'type': 'integer'},
    'month': {'label': 'Month', 'type': 'integer'},
    'day': {'label': 'Day of month', 'type': 'integer'},
    'week': {'label': 'Week of year', 'type': 'integer'},
    'iso_week_day': {'label': 'Day of week', 'type': 'enum', 'choices': iso_week_day_choices}
}

supported_conditions = {
    'string': {'exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'},
    'integer': {'exact', 'gt', 'gte', 'lt', 'lte', 'range'},
    'decimal': {'exact', 'gt', 'gte', 'lt', 'lte', 'range'},
    'date': {'exact', 'gt', 'gte', 'lt', 'lte', 'range'},
    # 'enum' and 'boolean' fields get special treatment
}

schema = {
    'meta': schema_meta,
    'fields': schema_fields
}

schema_model_lookup = {model._meta.model_name: model for model in schema_models}

@cache_control(max_age=86400)
@api_login_required
def custom_query_schema(request):
    return JsonResponse(schema)

@login_required
def custom_query(request):
    return render(request, 'custom_query.html')

def get_clean_field(start_table, subfield_list):
    current_type = start_table
    enum_choices = None
    subfields_cleaned = []
    for subfield in subfield_list:
        subfield_info = schema_fields[current_type][subfield]
        current_type = subfield_info['type']
        enum_choices = subfield_info.get('choices', None)
        subfields_cleaned.append(subfield)
    if len(subfields_cleaned) == 0:
        subfields_cleaned.append('id')
    return "__".join(subfields_cleaned), current_type, enum_choices

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

    start_model = schema_model_lookup.get(start_table, None)
    if start_model is None:
        raise SuspiciousOperation("Invalid starting table.")

    query_set = start_model.objects.all()

    # Parse and validate field selection
    # selected_fields: The list of fields to export.
    selected_fields = []
    # model_types: Same length as selected_fields, specifies whether each field should be passed through verbatim (= None)
    # or whether its string representation should be looked up from an enum (= ('enum', choices))
    # or whether its string representation should be looked up from the DB in a separate query (= ('model', model name))
    model_types = []
    try:
        if len(body["fields"]) == 0:
            body["fields"] = [[]]
        for subfield_list in body["fields"]:
            field_text, field_type, enum_choices = get_clean_field(start_table, subfield_list)
            selected_fields.append(field_text)
            if enum_choices is not None: # is enum
                model_types.append(('enum', dict(enum_choices)))
            elif field_type in schema_meta and not schema_meta[field_type].get('fakeTable', False): # is foreign key
                model_types.append(('model', field_type))
            else:
                model_types.append(None)

    except TypeError:
        raise SuspiciousOperation("Invalid field selection.")
    except KeyError:
        raise SuspiciousOperation("Invalid field selection.")

    # Filter the rows
    try:
        for filter_section in body["filters"]:
            filter_field, field_type, enum_choices = get_clean_field(start_table,filter_section["field"])
            cond_q = Q()
            for filter_condition in filter_section["conditions"]:
                id = filter_condition["id"]
                if field_type == "boolean":
                    cond_dict = {}
                    cond_dict[filter_field + "__exact"] = (id == "True")
                    cond_q |= Q(**cond_dict)
                elif enum_choices is not None:
                    cond_dict = {}
                    cond_dict[filter_field + "__exact"] = id
                    cond_q |= Q(**cond_dict)
                else:
                    if (field_type not in supported_conditions) or (id not in supported_conditions[field_type]):
                        raise SuspiciousOperation("Invalid condition.")
                    args = filter_condition["args"]
                    # Hack to avoid ValueError: year out of range
                    if filter_field.endswith("__year") and field_type == "integer":
                        for i in range(len(args)):
                            args[i] = max(1, int(args[i]))
                    if len(args) == 1:
                        args = args[0]
                    cond_dict = {}
                    cond_dict[filter_field + "__" + id] = args
                    cond_q |= Q(**cond_dict)
            query_set = query_set.filter(cond_q)
    except TypeError:
        raise SuspiciousOperation("Invalid condition.")
    except KeyError:
        raise SuspiciousOperation("Invalid condition.")
    except ValueError:
        raise SuspiciousOperation("Invalid condition.")

    # Get the results
    results = list(list(row) for row in query_set.values_list(*selected_fields))

    # Replace foreign-key IDs and enums with string representations
    for field_index, model_type in enumerate(model_types):
        if model_type is not None:
            if model_type[0] == 'model':
                model_type = model_type[1]
                # Get all of the IDs that need to be fetched
                ids = set(row[field_index] for row in results)
                # Fetch the models with those IDs
                models = {instance.pk: str(instance) for instance in schema_model_lookup[model_type].objects.all().filter(pk__in=ids)}
                # For each row, replace the ID with the string representation
                for row in results:
                    if row[field_index] is not None:
                        row[field_index] = models.get(row[field_index], None)
            elif model_type[0] == 'enum':
                choices = model_type[1]
                # For each row, replace the ID with the string representation
                for row in results:
                    if row[field_index] is not None:
                        row[field_index] = choices.get(row[field_index], str(row[field_index]))

    return JsonResponse({
        'headings': selected_fields,
        'data': results
    })