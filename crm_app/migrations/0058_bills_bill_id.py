# Generated by Django 2.0.9 on 2019-01-03 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0057_remove_bills_bill_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bills',
            name='bill_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
