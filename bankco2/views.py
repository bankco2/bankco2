from rest_framework import viewsets

from bankco2.models import Step
from bankco2.serializers import StepSerializer


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
