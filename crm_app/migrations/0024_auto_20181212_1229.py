# Generated by Django 2.0.9 on 2018-12-12 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0023_auto_20181211_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followed_history',
            name='lead_id',
        ),
        migrations.DeleteModel(
            name='Followed_History',
        ),
    ]
