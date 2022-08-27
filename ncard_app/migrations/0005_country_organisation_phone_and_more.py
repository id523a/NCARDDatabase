# Generated by Django 4.1 on 2022-08-27 13:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import pytz

def add_countries(apps, schema_editor):
    Country = apps.get_model('ncard_app', 'Country')
    db_alias = schema_editor.connection.alias
    countries = []
    for code, name in pytz.country_names.items():
        countries.append(Country(code=code, name=name))
    Country.objects.using(db_alias).bulk_create(countries)

def reverse_add_countries(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0004_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[A-Z]{2}$', 'Country code must be two upper-case letters, e.g. AU')], verbose_name='country code')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.RunPython(add_countries, reverse_add_countries),
        migrations.AddField(
            model_name='organisation',
            name='phone',
            field=models.CharField(blank=True, max_length=25, validators=[django.core.validators.RegexValidator('^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')], verbose_name='phone'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='primary_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='organisations_primary_contact', to='ncard_app.person'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='twitter_handle',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator('^$|^@[A-Za-z0-9_]+$', 'Twitter handle must begin with an @ and only contain letters, digits and underscores.')], verbose_name='Twitter handle'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='type',
            field=models.IntegerField(choices=[(0, '-'), (1, 'Health/Education/Research'), (2, 'Funding Agency'), (3, 'Community'), (4, 'Service Provider')], default=0, verbose_name='type'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='website',
            field=models.URLField(blank=True, verbose_name='website'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='type')),
                ('year', models.PositiveSmallIntegerField(verbose_name='year')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('journal', models.CharField(max_length=255, verbose_name='journal')),
                ('journal_ISSN', models.CharField(max_length=255, verbose_name='journal ISSN')),
                ('volume', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='volume')),
                ('page_start', models.PositiveIntegerField(blank=True, null=True, verbose_name='start page')),
                ('page_end', models.PositiveIntegerField(blank=True, null=True, verbose_name='end page')),
                ('open_access_status', models.IntegerField(choices=[(0, 'None'), (1, 'Open'), (2, 'Closed'), (3, 'Indeterminate'), (4, 'Embargoed')], default=0)),
                ('doi', models.CharField(max_length=255, verbose_name='doi')),
                ('electronic_ISBN', models.CharField(blank=True, max_length=255, verbose_name='electronic ISBN')),
                ('print_ISBN', models.CharField(blank=True, max_length=255, verbose_name='print ISBN')),
                ('abstract', models.TextField(blank=True, verbose_name='abstract')),
                ('citation', models.TextField(blank=True, verbose_name='citation (Vancouver)')),
                ('source_ID', models.CharField(blank=True, max_length=50, verbose_name='source ID')),
                ('ncard_publication', models.BooleanField(default=True, verbose_name='NCARD publication')),
                ('contributors', models.ManyToManyField(to='ncard_app.person')),
            ],
            options={
                'ordering': ['-year'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='type')),
                ('date', models.DateField(verbose_name='date')),
                ('number_attendees', models.IntegerField(verbose_name='number of attendees')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('detail', models.TextField(verbose_name='detail')),
                ('participants', models.TextField(verbose_name='participants')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='location')),
                ('lead_contacts', models.ManyToManyField(blank=True, to='ncard_app.person')),
                ('lead_organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='ncard_app.organisation')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Prize'), (2, 'Scholarship')], verbose_name='type')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('status', models.IntegerField(choices=[(1, 'Awardee'), (2, 'Nominee'), (3, 'Finalist')], default=1, verbose_name='award status')),
                ('detail', models.TextField(blank=True, verbose_name='detail')),
                ('year', models.PositiveSmallIntegerField(verbose_name='year')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='awards', to='ncard_app.organisation')),
                ('recipients', models.ManyToManyField(to='ncard_app.person')),
            ],
            options={
                'ordering': ['-year'],
            },
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='country',
            field=models.ForeignKey(default='AU', on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='ncard_app.country'),
        ),
    ]
