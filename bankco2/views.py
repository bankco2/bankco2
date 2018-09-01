from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.response import Response

from bankco2.models import Step
from bankco2.serializers import StepSerializer

from django.shortcuts import render


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Step.objects.update_or_create(
            device_id=serializer.data.get('device_id'),
            defaults={
                'count': serializer.data.get('count'),
                'step_date': serializer.data.get('step_date')
            }
        )

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class MobileMainView(TemplateView):
    template_name = 'main.html'


class AnimalView(TemplateView):
    template_name = 'animal.html'


class IndexView(TemplateView):
    template_name = 'index.html'
