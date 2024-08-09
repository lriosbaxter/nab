from django.contrib.auth.models import AbstractUser
from django.db import models


class Folder(models.Model):
    name_source = models.CharField(max_length=50, blank=True, null=True)
    type_folder = models.CharField(max_length=50, blank=True, null=True)


class Script(models.Model):
    source_folder_id = models.ForeignKey(Folder, blank=True,
                                         null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    repository_name = models.CharField(max_length=50, blank=True, null=True)
    py_archive_name = models.CharField(max_length=75, blank=True, null=True)
    type_script = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    source_folder_id = models.ForeignKey(Folder, blank=True,
                                         null=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
