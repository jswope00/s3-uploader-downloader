# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3uploader_downloader', '0010_auto_20170830_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileuploadandurl',
            name='course_level',
            field=models.CharField(max_length=35, null=True),
        ),
    ]
