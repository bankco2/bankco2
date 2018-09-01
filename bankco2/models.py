from django.contrib.auth.models import User
from django.db import models


class Animal(models.Model):
    code = models.CharField(max_length=16)
    image = models.FileField(null=True, blank=True)
    score = models.FloatField(default=1)


class Device(models.Model):
    device_id = models.CharField(max_length=100, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class CustomUser(User):
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL)
    animal = models.ManyToManyField(Animal)


class Step(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    count = models.IntegerField()
    step_date = models.DateField()


