# Generated by Django 3.2.7 on 2022-03-12 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OptionApp', '0005_auto_20220312_1558'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TradeList',
            new_name='TradeBook',
        ),
    ]
