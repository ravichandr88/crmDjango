# Generated by Django 2.0.9 on 2019-01-03 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0052_bills'),
    ]

    operations = [
        migrations.AddField(
            model_name='bills',
            name='bill_id',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
