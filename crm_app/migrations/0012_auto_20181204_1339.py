# Generated by Django 2.0.9 on 2018-12-04 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0011_auto_20181204_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead_data',
            name='user_detail',
        ),
        migrations.RemoveField(
            model_name='reporter_list',
            name='report_to',
        ),
        migrations.RemoveField(
            model_name='reporter_list',
            name='reporter_id',
        ),
        migrations.DeleteModel(
            name='Lead_Data',
        ),
        migrations.DeleteModel(
            name='Reporter_List',
        ),
        migrations.DeleteModel(
            name='User_Details',
        ),
    ]
