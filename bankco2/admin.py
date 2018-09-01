from django.contrib import admin

from bankco2.models import Step, Device, Animal


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('device', 'step_date', 'count')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'score')
