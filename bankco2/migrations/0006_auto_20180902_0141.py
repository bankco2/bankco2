# Generated by Django 2.1.1 on 2018-09-01 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('account', '0002_email_max_length'),
        ('socialaccount', '0003_extra_data_default_dict'),
        ('bankco2', '0005_auto_20180902_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='animal',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='device',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='device',
            name='animal',
            field=models.ManyToManyField(to='bankco2.Animal'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(default='dU2ZHFwz_xo', max_length=100),
        ),
        migrations.AlterField(
            model_name='step',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bankco2.Device'),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
