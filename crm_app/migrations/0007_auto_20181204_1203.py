# Generated by Django 2.0.9 on 2018-12-04 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0006_auto_20181204_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_lead_list',
            name='User_detail',
        ),
        migrations.DeleteModel(
            name='User_Details',
        ),
        migrations.DeleteModel(
            name='User_Lead_List',
        ),
    ]