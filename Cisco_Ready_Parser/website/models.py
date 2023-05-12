# from django.db import models
# from django.core.files.storage import FileSystemStorage
#
# fs = FileSystemStorage(location="/media/folders")
#
#
# class UploadedFolder(models.Model):
#     folder = models.FileField(storage=fs, upload_to="")
#     start_date = models.DateField()
#     end_date = models.DateField()
#
#
# class UploadedFile(models.Model):
#     name = models.CharField(max_length=255)
#     file = models.FileField(upload_to="uploads/")
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
