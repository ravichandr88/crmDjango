# Generated by Django 2.0.9 on 2018-12-11 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0021_lead_follow_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead_follow_table',
            name='lead_id',
        ),
        migrations.RemoveField(
            model_name='lead_follow_table',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Lead_Follow_Table',
        ),
    ]
