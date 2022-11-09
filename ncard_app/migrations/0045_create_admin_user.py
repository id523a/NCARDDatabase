from django.db import migrations
from django.conf import settings
import os

def create_super_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if User.objects.all().filter(username='admin').exists():
        print(" User admin already exists")
    else:
        with open(os.path.join(settings.BASE_DIR, 'NCARDDatabase', 'secrets', 'admin_password.txt'), mode='r') as f:
            superuser_password = f.read()
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@localhost',
            password=superuser_password)
        superuser.save()
        print(" User admin created")

def nop(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('ncard_app', '0044_alter_publication_source_id'),
        ('auth', '0012_alter_user_first_name_max_length')
    ]
    operations = [
        migrations.RunPython(create_super_user, nop)
    ]
