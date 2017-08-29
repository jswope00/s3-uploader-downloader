# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class FileUploadAndUrl(models.Model):

    src_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_uploaded = models. DateTimeField()
    uploaded_by = models.CharField(max_length=200)
    unit_id = models.CharField(max_length=35)
    folder_name = models.CharField(max_length=200)
    is_url = models.BooleanField(default=False)

class FileAndUrl():

    def create_record(self, src_name, title, description, uploaded_by, unit_id, folder_name, is_url):
            upload_date = datetime.now()
            upload_record = FileUploadAndUrl(
                src_name=src_name,
                title=title,
                description=description,
                date_uploaded=upload_date,
                uploaded_by=uploaded_by,
                unit_id=unit_id,
                folder_name=folder_name,
                is_url=is_url)
            upload_record.save()
            return {"status": "success"}

    def update_record(self, row_id, src_name, title, description, is_url):
        row = FileUploadAndUrl.objects.get(id=row_id)
        row.title=title
        row.description=description
        if is_url:
            row.src_name=src_name
        row.save()
        

    def delete_record(self, row_id):
            row = FileUploadAndUrl.objects.get(id=row_id)
            row.delete()
            return {"status": "success"}

    def get_file_path(self, file_id):
        file = FileUploadAndUrl.objects.get(id=file_id)
        if file.folder_name == "":
            return file.unit_id+"/"+file.src_name
        else:
            return file.folder_name+"/"+file.unit_id+"/"+file.src_name