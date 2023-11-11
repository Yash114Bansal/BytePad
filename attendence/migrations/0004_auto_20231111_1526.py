# Generated by Django 3.2.20 on 2023-11-11 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('attendence', '0003_auto_20231111_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancesheet',
            old_name='batch',
            new_name='assignment',
        ),
        migrations.AlterUniqueTogether(
            name='attendancesheet',
            unique_together={('assignment', 'date')},
        ),
    ]