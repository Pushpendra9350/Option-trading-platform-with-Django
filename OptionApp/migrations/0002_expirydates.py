# Generated by Django 3.2.7 on 2022-03-12 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OptionApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiryDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiry_date', models.CharField(max_length=100)),
            ],
        ),
    ]
