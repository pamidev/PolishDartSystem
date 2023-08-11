# Generated by Django 4.2.4 on 2023-08-05 19:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TournamentMatch',
            new_name='Match',
        ),
        migrations.RenameModel(
            old_name='TrainingMatch',
            new_name='Training',
        ),
        migrations.AlterModelOptions(
            name='training',
            options={},
        ),
    ]
