# Generated by Django 2.0.9 on 2018-12-04 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('user_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter_list', to='crm_app.User_Details')),
            ],
        ),
    ]
