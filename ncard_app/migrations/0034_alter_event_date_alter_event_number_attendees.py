# Generated by Django 4.1 on 2022-10-15 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0033_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='number_attendees',
            field=models.TextField(blank=True, null=True, verbose_name='number of Attendees'),
        ),
    ]
