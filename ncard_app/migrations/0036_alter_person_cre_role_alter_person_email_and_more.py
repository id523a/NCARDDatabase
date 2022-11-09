# Generated by Django 4.1 on 2022-10-15 12:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0035_alter_publication_publication_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='cre_role',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='CRE Role'),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Primary Email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='email2',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Secondary Email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='employers',
            field=models.ManyToManyField(blank=True, null=True, related_name='employees', to='ncard_app.organisation'),
        ),
        migrations.AlterField(
            model_name='person',
            name='google_scholar',
            field=models.URLField(blank=True, null=True, verbose_name='Google Scholar'),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_line1',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Line 1'),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_line2',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Line 2'),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_line3',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Line 3'),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_postcode',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Postcode'),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_state',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='State (abbrev.)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_suburb',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Suburb'),
        ),
        migrations.AlterField(
            model_name='person',
            name='linkedin',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn (URL)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='loop_profile',
            field=models.URLField(blank=True, null=True, verbose_name='Loop Profile'),
        ),
        migrations.AlterField(
            model_name='person',
            name='middle_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='orcid_id',
            field=models.CharField(blank=True, max_length=37, null=True, validators=[django.core.validators.RegexValidator('^$|^https://orcid\\.org/\\d{4}-\\d{4}-\\d{4}-\\d{3}(\\d|X)$', 'ORCID identifier must be a full URL, in this format: https://orcid.org/XXXX-XXXX-XXXX-XXXX')], verbose_name='ORCID iD'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone_home',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')], verbose_name='phone (Home)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone_mobile',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')], verbose_name='phone (Mobile)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone_office',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')], verbose_name='phone (Office)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='profile_url',
            field=models.URLField(blank=True, null=True, verbose_name='Profile URL'),
        ),
        migrations.AlterField(
            model_name='person',
            name='project',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='researchgate',
            field=models.URLField(blank=True, null=True, verbose_name='ResearchGate'),
        ),
        migrations.AlterField(
            model_name='person',
            name='surname',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='twitter',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator('^$|^@[A-Za-z0-9_]+$', 'Twitter handle must begin with an @ and only contain letters, digits and underscores.')], verbose_name='Twitter Handle'),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_line1',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Line 1'),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_line2',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Line 2'),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_line3',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Line 3'),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_postcode',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Postcode'),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_state',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='State (abbrev.)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_suburb',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Suburb'),
        ),
        migrations.AlterField(
            model_name='person',
            name='wos_researcher_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='WoS ResearcherID'),
        ),
    ]
