# Generated by Django 2.0.9 on 2019-01-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0054_auto_20190103_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='bill_id',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]