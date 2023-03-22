from rest_framework import serializers
from .models import MonthlyDataModel

class MonthlyDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyDataModel
        fields = '__all__'