# Generated by Django 3.2.7 on 2022-03-22 07:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OptionApp', '0014_auto_20220322_0719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='daywisesummery',
            old_name='p_n_l',
            new_name='buy_p_n_l',
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='sell_p_n_l',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='daywisesummery',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 7, 48, 49, 700544, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 7, 48, 49, 700356, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='half_exit_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 7, 48, 49, 700349, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 7, 48, 49, 700342, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 7, 48, 49, 700093, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='half_exit_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 7, 48, 49, 700085, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 7, 48, 49, 700072, tzinfo=utc)),
        ),
    ]
