# Generated by Django 2.0.9 on 2018-12-15 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0031_auto_20181215_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice_list',
            name='invc_id',
            field=models.CharField(default='asd', max_length=20),
        ),
    ]
