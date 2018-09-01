from django.views.generic import TemplateView
from rest_framework import viewsets

from bankco2.models import Step
from bankco2.serializers import StepSerializer


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class IndexView(TemplateView):
    template_name = 'index.html'
