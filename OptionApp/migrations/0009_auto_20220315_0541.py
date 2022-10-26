# Generated by Django 3.2.7 on 2022-03-15 05:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OptionApp', '0008_auto_20220315_0537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activetrade',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 5, 41, 16, 209490, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='activetrade',
            name='half_exit_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 5, 41, 16, 209455, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='activetrade',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 5, 41, 16, 209483, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='activetrade',
            name='token',
            field=models.CharField(default='00000', max_length=100),
        ),
        migrations.AlterField(
            model_name='daywisesummery',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 5, 41, 16, 209669, tzinfo=utc)),
        ),
    ]
