from django.contrib.auth.models import User
from django.db import models


class BankCo2User(User):
    device_id = models.CharField(max_length=512)
    nick_name = models.CharField(max_length=512)


class Step(models.Model):
    user = models.ForeignKey(BankCo2User, on_delete=models.CASCADE)
    count = models.IntegerField()
    step_date = models.DateField()
