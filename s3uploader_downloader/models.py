# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class FileUpload(models.Model):

    file_name = models.CharField(max_length=200)
    file_title = models.CharField(max_length=200)
    description = models.TextField()
    date_uploaded = models. DateTimeField()
    uploaded_by = models.CharField(max_length=200)
    unit_id = models.CharField(max_length=35)
    folder_name = models.CharField(max_length=200,null=True)


class FileUploader():

    def create_record(self, file_name, file_title, description, uploaded_by, unit_id, folder_name):
            upload_date = datetime.now()
            upload_record = FileUpload(
                file_name=file_name,
                file_title=file_title,
                description=description,
                date_uploaded=upload_date,
                uploaded_by=uploaded_by,
                unit_id=unit_id,
                folder_name=folder_name)
            upload_record.save()
            return {"status": "success"}

    def update_record(self, file_id, file_title, description):
        file = FileUpload.objects.get(id=file_id)
        file.file_title=file_title
        file.description=description
        file.save()

    def delete_record(self, file_id):
            file = FileUpload.objects.get(id=file_id)
            file.delete()
            return {"status": "success"}

    def get_file_path(self, file_id):
        file = FileUpload.objects.get(id=file_id)
        if file.folder_name == "":
            return file.unit_id+"/"+file.file_name
        else:
            return file.folder_name+"/"+file.unit_id+"/"+file.file_name