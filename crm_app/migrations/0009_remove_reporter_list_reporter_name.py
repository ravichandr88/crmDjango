# Generated by Django 2.0.9 on 2018-12-04 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0008_auto_20181204_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporter_list',
            name='reporter_name',
        ),
    ]