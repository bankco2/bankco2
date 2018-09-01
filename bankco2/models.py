from django.contrib.auth.models import User
from django.db import models


class Animal(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(null=True, blank=True)
    score = models.FloatField(default=1)    # 뽑기확률.. ?

    def __str__(self):
        return self.name


class Device(models.Model):
    device_id = models.CharField(max_length=100, blank=False, null=False,
                                 default='dU2ZHFwz_xo')

    created_at = models.DateTimeField(auto_now_add=True, null=False,
                                      blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    animal = models.ManyToManyField(Animal)

    def __str__(self):
        return self.device_id


class Step(models.Model):
    device = models.ForeignKey(Device, null=True, blank=True,
                               on_delete=models.CASCADE)
    count = models.IntegerField()

    step_date = models.DateField()
    draw_flag = models.BooleanField(default=False)

    def __str__(self):
        return "%s/%s" % (self.device.device_id, self.step_date)
