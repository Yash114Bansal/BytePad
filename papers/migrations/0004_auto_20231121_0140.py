# Generated by Django 3.2.20 on 2023-11-20 20:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0003_mycollections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplepaper',
            name='file',
            field=models.FileField(upload_to='uploads/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'])]),
        ),
        migrations.AlterField(
            model_name='samplepapersolution',
            name='file',
            field=models.FileField(upload_to='uploads/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'])]),
        ),
    ]