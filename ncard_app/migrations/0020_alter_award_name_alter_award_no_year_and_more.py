# Generated by Django 4.1 on 2022-10-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0019_alter_students_options_alter_award_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Awawrd Name'),
        ),
        migrations.AlterField(
            model_name='award',
            name='no_year',
            field=models.DecimalField(blank=True, decimal_places=1, default=1.0, max_digits=10, null=True, verbose_name='Concurrent Years'),
        ),
        migrations.AlterField(
            model_name='award',
            name='status',
            field=models.IntegerField(choices=[(1, 'Awardee'), (2, 'Nominee'), (3, 'Finalist')], default=1, verbose_name='Award Status'),
        ),
        migrations.AlterField(
            model_name='award',
            name='year',
            field=models.PositiveSmallIntegerField(verbose_name='Year Established'),
        ),
    ]
