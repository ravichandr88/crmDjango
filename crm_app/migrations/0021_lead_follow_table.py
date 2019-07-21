# Generated by Django 2.0.9 on 2018-12-11 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0020_followed_history_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead_Follow_Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_asign_flow', to='crm_app.Lead_List')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_lead_assign_flow', to='crm_app.User_Details')),
            ],
        ),
    ]
