# Generated by Django 5.0.2 on 2024-03-23 17:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_match_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 23, 18, 51, 43, 750894)),
        ),
    ]