# Generated by Django 3.2.20 on 2023-11-11 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendence', '0004_auto_20231111_1526'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendancesheet',
            unique_together=set(),
        ),
    ]