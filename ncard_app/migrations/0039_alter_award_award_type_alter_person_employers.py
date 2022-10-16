# Generated by Django 4.1 on 2022-10-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0038_alter_event_number_attendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='award_type',
            field=models.IntegerField(choices=[(1, 'Prize'), (2, 'Scholarship'), (3, 'Award'), (4, 'Grant')], verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='person',
            name='employers',
            field=models.ManyToManyField(blank=True, related_name='employees', to='ncard_app.organisation'),
        ),
    ]
