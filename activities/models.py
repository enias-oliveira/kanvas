from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    repo = models.CharField(max_length=255)
    grade = models.IntegerField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
