# Generated by Django 2.0.9 on 2019-01-05 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0059_auto_20190104_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_date', models.DateField()),
                ('pay_amount', models.CharField(max_length=15)),
                ('inv_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instlmnts_lst', to='crm_app.Invoice_List')),
            ],
        ),
    ]
