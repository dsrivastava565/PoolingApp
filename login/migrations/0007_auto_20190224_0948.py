# Generated by Django 2.1.7 on 2019-02-24 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_startpooling_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startpooling',
            name='time_end',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='startpooling',
            name='time_start',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
