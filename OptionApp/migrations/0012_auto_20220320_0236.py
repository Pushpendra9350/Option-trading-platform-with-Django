# Generated by Django 3.2.7 on 2022-03-20 02:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OptionApp', '0011_auto_20220320_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daywisesummery',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 35, 58, 837591, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 35, 58, 837404, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='half_exit_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 35, 58, 837398, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 35, 58, 837391, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 35, 58, 837143, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='half_exit_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 35, 58, 837137, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 35, 58, 837123, tzinfo=utc)),
        ),
    ]
