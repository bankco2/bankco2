from django.utils.timezone import localtime
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.response import Response

from bankco2.models import Step, Device
from bankco2.serializers import StepSerializer


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_id = serializer.data.get('device_id')

        device = Device.objects.get_or_create(device_id=device_id)

        Step.objects.update_or_create(
            device=device,
            step_date=serializer.data.get('step_date'),
            defaults={
                'count': serializer.data.get('count'),
            }
        )

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class MobileMainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        device_id = self.request.GET.get("device_id")

        time = localtime()

        step = Step.objects.filter(device__device_id=device_id, step_date=time.strftime("Y-m-d"))

        return {
            "device_id": device_id,
            "step": step
        }


class AnimalView(TemplateView):
    template_name = 'animal.html'


class IndexView(TemplateView):
    template_name = 'index.html'
