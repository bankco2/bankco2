from django.views.generic import TemplateView
from rest_framework import viewsets

from bankco2.models import Step
from bankco2.serializers import StepSerializer

from django.shortcuts import render


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class IndexView(TemplateView):
    template_name = 'login.html'
