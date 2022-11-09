# Generated by Django 4.1 on 2022-10-16 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0042_alter_award_link_alter_award_notes_alter_award_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='link'),
        ),
        migrations.AlterField(
            model_name='award',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='notes'),
        ),
    ]
