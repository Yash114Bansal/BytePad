# Generated by Django 3.2.20 on 2023-11-10 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SamplePaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='uploads/')),
                ('year', models.IntegerField()),
                ('semester', models.IntegerField()),
                ('courses', models.ManyToManyField(to='accounts.Course')),
            ],
        ),
    ]
