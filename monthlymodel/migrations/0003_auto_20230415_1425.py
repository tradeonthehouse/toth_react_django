# Generated by Django 3.2.13 on 2023-04-15 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthlymodel', '0002_strategymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategymodel',
            name='Date_Created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='strategymodel',
            name='Strategy_Type',
            field=models.TextField(null=True),
        ),
    ]
