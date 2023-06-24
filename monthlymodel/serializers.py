from rest_framework import serializers
from .models import MonthlyDataModel
from .models import StrategyModel
from .models import BrokerModel
from .models import DataStrategyMappingModel
from .models import AlertDataModel,PositionalDataModel

class MonthlyDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyDataModel
        fields = '__all__'
        
class StrategyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyModel
        fields = '__all__'
        
class BrokerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerModel
        fields = '__all__'
        
class DataStrategyMappingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataStrategyMappingModel
        fields = '__all__'
        
class AlertDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertDataModel
        fields = '__all__'
        
class PositionalDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionalDataModel
        fields = '__all__'