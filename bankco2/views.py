from django.utils.timezone import localtime
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.response import Response

from bankco2.models import Step, Device, Animal
from bankco2.serializers import StepSerializer

import random


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_id = request.data.get('device_id')

        (device, is_created) = Device.objects.get_or_create(device_id=device_id)

        Step.objects.update_or_create(
            device=device,
            step_date=serializer.data.get('step_date'),
            defaults={
                'count': serializer.data.get('count'),
            }
        )

        headers = self.get_success_headers(serializer.data)

        if is_created:
            response_status = status.HTTP_201_CREATED
        else:
            response_status = status.HTTP_200_OK

        return Response(serializer.data, status=response_status, headers=headers)


class MobileMainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        device_id = self.request.GET.get("device_id")

        time = localtime()

        if device_id:
            step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("%Y-%m-%d"))
        else:
            step = None

        return {
            "device_id": device_id,
            "step": step
        }


class AnimalView(TemplateView):
    template_name = 'animal.html'

    def get_context_data(self, **kwargs):
        device_id = self.request.GET.get("device_id")

        animals = Device.objects.filter(device=device_id)

        return {
            "animals": animals
        }


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        device_id = self.request.GET.get("device_id")

        time = localtime()

        step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("Y-m-d"))
        context['step'] = step

        return context


def draw(request, device_id):
    time = localtime()

    animals = Animal.objects.all()
    choiced_animal = random.choice(animals)

    step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("Y-m-d")).first()
    if step and step.count >= 10000:
        step.device.animal.add(choiced_animal)
        step.device.save()

        ret = {
            "status": 200,
            "name": choiced_animal.name,
            "image_url": choiced_animal.image
        }
    else:
        ret = {
            "status": 400,
        }

    return ret