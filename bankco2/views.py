import json
from datetime import timedelta

from django.http import HttpResponse
from django.utils.timezone import localtime
from django.views.generic import TemplateView, ListView
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
        step_date = request.data.get('step_date')

        if step_date == "1970-01-01":
            time = localtime()
            step_date = time.strftime("%Y-%m-%d")

        (device, is_created) = Device.objects.get_or_create(device_id=device_id)

        Step.objects.update_or_create(
            device=device,
            step_date=step_date,
            defaults={
                'count': request.data.get('count'),
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
            step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("%Y-%m-%d")).first()
        else:
            step = None

        context.update({
            "device_id": device_id,
            "step": step
        })

        return context


class RankView(TemplateView):
    template_name = 'rank.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        device_id = self.request.GET.get("device_id")

        time = localtime()

        steps = Step.objects.filter(step_date=time.strftime("%Y-%m-%d")).order_by('-count')[:10]

        ranking = []
        rank = 1
        in_rank_flag = False

        for step in steps:
            if step.device.device_id == device_id:
                in_rank_flag = True

            ranking.append({
                "rank": rank,
                "device_id": step.device.device_id,
                "count": step.count,
            })

            rank = rank + 1

        if device_id and not in_rank_flag:
            step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("%Y-%m-%d")).first()

            ranking.append({
                "rank": "-",
                "device_id": step.device.device_id,
                "count": step.count,
            })


        context.update({
            "device_id": device_id,
            "today": time,
            "ranking": ranking
        })

        return context


class HistoryView(TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        device_id = self.request.GET.get("device_id")

        steps = []

        for i in range(-6, 1):
            time = localtime() + timedelta(days=i)

            step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("%Y-%m-%d")).first()

            if step:
                steps.append(step)
            else:
                steps.append({
                    "step_date": time,
                    "count": 0
                })

        context.update({
            "device_id": device_id,
            "steps": steps
        })

        return context


class AnimalView(ListView):
    template_name = 'animal.html'
    queryset = Animal.objects.all()


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        device_id = self.request.GET.get("device_id")

        time = localtime()

        step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("%Y-%m-%d"))
        context.update({
            'step': step
        })

        return context


def draw(request, device_id):
    time = localtime()

    animals = Animal.objects.all()
    choiced_animal = random.choice(animals)

    step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("%Y-%m-%d"), draw_flag=False).first()
    if step and step.count >= 10000:
        step.device.animal.add(choiced_animal)

        step.draw_flag = True
        step.save()

        ret = {
            "status": 200,
            "name": choiced_animal.name,
        }

        if choiced_animal.image:
            ret.update({
               "image_url": choiced_animal.image.url
            })
    else:
        ret = {
            "status": 400,
        }

    return HttpResponse(json.dumps(ret))