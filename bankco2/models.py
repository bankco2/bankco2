from django.contrib.auth.models import User
from django.db import models


class Step(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField()
    step_date = models.DateField()


