# Generated by Django 3.2.20 on 2023-11-05 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0002_auto_20231102_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplepaper',
            name='year',
            field=models.IntegerField(),
        ),
    ]
