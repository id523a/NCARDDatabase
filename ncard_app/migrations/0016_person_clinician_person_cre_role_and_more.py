# Generated by Django 4.1 on 2022-10-01 04:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0015_delete_contactrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='clinician',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='cre_role',
            field=models.CharField(blank=True, max_length=15, verbose_name='CRE role'),
        ),
        migrations.AddField(
            model_name='person',
            name='display_on_website',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes'), (2, 'Yes - student')], default=0),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='person',
            name='email2',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email 2'),
        ),
        migrations.AddField(
            model_name='person',
            name='employers',
            field=models.ManyToManyField(blank=True, to='ncard_app.organisation'),
        ),
        migrations.AddField(
            model_name='person',
            name='google_scholar',
            field=models.URLField(blank=True, verbose_name='Google Scholar'),
        ),
        migrations.AddField(
            model_name='person',
            name='linkedin',
            field=models.URLField(blank=True, verbose_name='LinkedIn'),
        ),
        migrations.AddField(
            model_name='person',
            name='location',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='person',
            name='loop_profile',
            field=models.URLField(blank=True, verbose_name='Loop profile'),
        ),
        migrations.AddField(
            model_name='person',
            name='ncard_relation',
            field=models.IntegerField(choices=[(1, 'Core team'), (2, 'Affiliate'), (3, 'Collaborator'), (4, 'Community / Consumer'), (5, 'Advocate'), (6, 'Govt / Industry'), (0, 'Other')], default=0, verbose_name='relationship with NCARD'),
        ),
        migrations.AddField(
            model_name='person',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='orcid_id',
            field=models.CharField(blank=True, max_length=37, validators=[django.core.validators.RegexValidator('^$|^https://orcid\\.org/\\d{4}-\\d{4}-\\d{4}-\\d{3}(\\d|X)$', 'ORCID identifier must be a full URL, in this format: https://orcid.org/XXXX-XXXX-XXXX-XXXX')], verbose_name='ORCID iD'),
        ),
        migrations.AddField(
            model_name='person',
            name='organisation_other',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_records_other', to='ncard_app.organisation', verbose_name='organisation (other)'),
        ),
        migrations.AddField(
            model_name='person',
            name='organisation_primary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_records_primary', to='ncard_app.organisation', verbose_name='organisation (primary)'),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_home',
            field=models.CharField(blank=True, max_length=25, validators=[django.core.validators.RegexValidator('^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')], verbose_name='phone (home)'),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_mobile',
            field=models.CharField(blank=True, max_length=25, validators=[django.core.validators.RegexValidator('^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')], verbose_name='phone (mobile)'),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_office',
            field=models.CharField(blank=True, max_length=25, validators=[django.core.validators.RegexValidator('^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')], verbose_name='phone (office)'),
        ),
        migrations.AddField(
            model_name='person',
            name='profile_url',
            field=models.URLField(blank=True, verbose_name='profile URL'),
        ),
        migrations.AddField(
            model_name='person',
            name='project',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='person',
            name='research_focus',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='person',
            name='researchgate',
            field=models.URLField(blank=True, verbose_name='ResearchGate'),
        ),
        migrations.AddField(
            model_name='person',
            name='scopus_id',
            field=models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, 'Value must not be negative.')], verbose_name='Scopus ID'),
        ),
        migrations.AddField(
            model_name='person',
            name='twitter',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator('^$|^@[A-Za-z0-9_]+$', 'Twitter handle must begin with an @ and only contain letters, digits and underscores.')], verbose_name='Twitter handle'),
        ),
        migrations.AddField(
            model_name='person',
            name='wos_researcher_id',
            field=models.CharField(blank=True, max_length=32, verbose_name='WoS ResearcherID'),
        ),
    ]
