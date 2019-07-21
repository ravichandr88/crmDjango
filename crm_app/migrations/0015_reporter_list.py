# Generated by Django 2.0.9 on 2018-12-06 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0014_auto_20181206_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporters_list', to='crm_app.User_Details')),
                ('reporter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.User_Details')),
            ],
        ),
    ]