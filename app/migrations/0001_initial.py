# Generated by Django 4.2.2 on 2023-07-07 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('company_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.TextField()),
                ('city', models.TextField()),
                ('introduction', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Job_finder',
            fields=[
                ('full_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('city', models.TextField()),
                ('date_of_birth', models.TextField()),
                ('introduction', models.TextField()),
            ],
        ),
    ]
