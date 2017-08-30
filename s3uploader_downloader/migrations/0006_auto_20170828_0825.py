# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3uploader_downloader', '0005_auto_20170828_0753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileuploadandurl',
            old_name='file_title',
            new_name='title',
        ),
    ]
