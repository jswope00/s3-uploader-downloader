# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3uploader_downloader', '0007_auto_20170829_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileuploadandurl',
            name='title',
            field=models.CharField(default='Title', max_length=200),
        ),
    ]
