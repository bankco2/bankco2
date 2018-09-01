from django.contrib.auth.models import User
from django.db import models


class Step(models.Model):
    device_id = models.CharField(max_length=255, default='default-id')
    count = models.IntegerField()
    step_date = models.DateField()


