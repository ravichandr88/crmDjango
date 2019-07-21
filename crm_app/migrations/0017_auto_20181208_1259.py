# Generated by Django 2.0.9 on 2018-12-08 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0016_auto_20181206_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followed_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Lead_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=300)),
                ('nxt_flw_dt', models.DateField(blank=True, default=None)),
                ('dob', models.DateField(blank=True, default=None)),
                ('status', models.CharField(max_length=10)),
                ('user_fllwng', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_list_data', to='crm_app.User_Details')),
            ],
        ),
        migrations.AddField(
            model_name='followed_history',
            name='lead_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_history', to='crm_app.Lead_List'),
        ),
    ]
