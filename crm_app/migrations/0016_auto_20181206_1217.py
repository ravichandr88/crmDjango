# Generated by Django 2.0.9 on 2018-12-06 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0015_reporter_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.User_Details')),
                ('report_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_list', to='crm_app.User_Details')),
            ],
        ),
        migrations.RemoveField(
            model_name='reporter_list',
            name='report_to',
        ),
        migrations.RemoveField(
            model_name='reporter_list',
            name='reporter_id',
        ),
        migrations.DeleteModel(
            name='Reporter_List',
        ),
    ]
