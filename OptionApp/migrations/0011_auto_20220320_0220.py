# Generated by Django 3.2.7 on 2022-03-20 02:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OptionApp', '0010_auto_20220315_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='daywisesummery',
            name='percentage',
        ),
        migrations.RemoveField(
            model_name='daywisesummery',
            name='total_quantity',
        ),
        migrations.RemoveField(
            model_name='daywisesummery',
            name='total_trades',
        ),
        migrations.RemoveField(
            model_name='daywisesummery',
            name='win_rate',
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='buy_percentage',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='sell_percentage',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='total_buy_quantity',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='total_buy_trades',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='total_sell_quantity',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='total_sell_trades',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='win_buy_rate',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daywisesummery',
            name='win_sell_rate',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='position',
            name='fill_exit_quantity',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='position',
            name='strategy',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='tradebook',
            name='fill_exit_quantity',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='tradebook',
            name='strategy',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='tradebook',
            name='token',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='daywisesummery',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 20, 28, 86461, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='daywisesummery',
            name='p_n_l',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='position',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 20, 28, 86270, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='half_exit_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 20, 28, 86264, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 20, 28, 86256, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='position',
            name='token',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='buy_price',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 20, 28, 86004, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='half_exit_price',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='half_exit_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 20, 28, 85997, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='half_quantity',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='order_type',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='p_n_l',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='quantity',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='sell_price',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 2, 20, 28, 85984, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='stoploss',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='symbol',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradebook',
            name='target',
            field=models.CharField(default='', max_length=100),
        ),
    ]
