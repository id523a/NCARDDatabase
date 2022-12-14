# Generated by Django 4.1 on 2022-08-25 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ncard_app', '0003_alter_contactrecord_phone_home_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.IntegerField(choices=[(0, '-'), (1, 'Pending'), (2, 'Active'), (3, 'Complete')], default=0)),
                ('funded', models.BooleanField(default=False)),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='ncard_app.person')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['name'], name='ncard_app_p_name_cc5b7d_idx'),
        ),
    ]
