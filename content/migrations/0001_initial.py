# Generated by Django 4.2.4 on 2023-09-11 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createt_at', models.DateField(default=datetime.date.today)),
                ('title', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=500)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
            ],
        ),
    ]
