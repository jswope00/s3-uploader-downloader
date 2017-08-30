# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=200)),
                ('file_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_uploaded', models.DateTimeField()),
                ('uploaded_by', models.CharField(max_length=200)),
                ('unit_id', models.CharField(max_length=35)),
                ('folder_name', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
