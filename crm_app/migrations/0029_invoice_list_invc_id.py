# Generated by Django 2.0.9 on 2018-12-15 11:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0028_auto_20181213_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice_list',
            name='invc_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]