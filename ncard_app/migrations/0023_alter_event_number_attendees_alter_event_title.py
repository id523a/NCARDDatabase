# Generated by Django 4.1 on 2022-10-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0022_merge_20221013_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='number_attendees',
            field=models.IntegerField(verbose_name='number of Attendees'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Event Title'),
        ),
    ]
