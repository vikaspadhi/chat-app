from operator import mod
from tokenize import group
from unicodedata import name
from django.db import models

# Create your models here.

class Chat(models.Model):
    msg = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey('Group',on_delete=models.CASCADE)

    def __str__(self):
        return self.msg

class Group(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name