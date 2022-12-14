# Generated by Django 3.2.7 on 2022-03-12 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SymbolAndTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('expiry', models.CharField(max_length=100)),
                ('strike', models.CharField(max_length=100)),
                ('lotsize', models.CharField(max_length=100)),
                ('instrumenttype', models.CharField(max_length=100)),
                ('exch_seg', models.CharField(max_length=100)),
                ('tick_size', models.CharField(max_length=100)),
            ],
        ),
    ]
