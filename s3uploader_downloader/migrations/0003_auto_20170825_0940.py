# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3uploader_downloader', '0002_auto_20170825_0642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileuploadandurl',
            old_name='file_name',
            new_name='src_name',
        ),
        migrations.AddField(
            model_name='fileuploadandurl',
            name='is_url',
            field=models.BooleanField(default=False),
        ),
    ]
