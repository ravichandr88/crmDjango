# Generated by Django 2.0.9 on 2018-12-12 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0025_followed_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followed_history',
            name='date',
            field=models.DateTimeField(),
        ),
    ]