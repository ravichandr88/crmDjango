# Generated by Django 2.0.9 on 2018-12-04 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0004_reporter_list_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporter_list',
            name='lead_detail',
        ),
    ]