# Generated by Django 3.2.20 on 2023-11-15 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_studentmodel_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default=None, upload_to='profile_pics/'),
        ),
    ]