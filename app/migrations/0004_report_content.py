# Generated by Django 4.2.2 on 2023-08-02 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_report"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="content",
            field=models.TextField(default=""),
        ),
    ]
