from django.contrib.auth.models import User
from django.db import models


class Step(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=512, default='-1')
    count = models.IntegerField()
    step_date = models.DateField()


class Animal(models.Model):
    animal_code = models.CharField(max_length=16)
    user = models.ManyToManyField(BankCo2User)
