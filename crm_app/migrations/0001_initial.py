# Generated by Django 2.0.9 on 2018-12-03 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('designation', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='User_Lead_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('User_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_list', to='crm_app.User_Details')),
            ],
        ),
    ]