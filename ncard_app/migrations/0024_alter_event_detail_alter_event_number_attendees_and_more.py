# Generated by Django 4.1 on 2022-10-13 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0023_alter_event_number_attendees_alter_event_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='detail',
            field=models.TextField(blank=True, verbose_name='details'),
        ),
        migrations.AlterField(
            model_name='event',
            name='number_attendees',
            field=models.IntegerField(blank=True, verbose_name='number of Attendees'),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.TextField(blank=True, verbose_name='participants'),
        ),
        migrations.AlterField(
            model_name='person',
            name='given_name',
            field=models.CharField(max_length=64, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='students',
            name='student_type',
            field=models.IntegerField(choices=[(1, 'Honours'), (2, 'PhD')], verbose_name='Student Type'),
        ),
        migrations.AlterField(
            model_name='students',
            name='title_topic',
            field=models.TextField(blank=True, verbose_name='Title Topic'),
        ),
        migrations.AlterField(
            model_name='students',
            name='year_end',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Year End'),
        ),
        migrations.AlterField(
            model_name='students',
            name='year_start',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Year Start'),
        ),
        migrations.DeleteModel(
            name='PersonAddress',
        ),
    ]
