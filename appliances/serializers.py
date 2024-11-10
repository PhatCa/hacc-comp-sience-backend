from rest_framework import serializers
from .models import Appliance

class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ['id', 'name', 'power_usage', 'is_on']
        
        
class PowerUsageSerializer(serializers.Serializer):
    total_power_usage = serializers.FloatField()