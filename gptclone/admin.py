from django.contrib import admin
from gptclone.models import Message, UploadedFile


# Register your models here.
admin.site.register(Message)
admin.site.register(UploadedFile)