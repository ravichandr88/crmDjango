# Generated by Django 2.0.9 on 2018-12-31 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0045_invoice_list_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followed_history',
            name='date',
            field=models.DateField(),
        ),
    ]