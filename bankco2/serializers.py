from rest_framework import serializers
from bankco2.models import Step, Device


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'

