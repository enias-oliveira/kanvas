from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    user_set = models.ManyToManyField(User)
