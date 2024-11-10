from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appliance
from .serializers import ApplianceSerializer, PowerUsageSerializer
from django.db.models import Sum

class ApplianceToggleView(APIView):
    def post(self, request, id):
        try:
            appliance = Appliance.objects.get(id=id)
            action = request.data.get('action')
            
            if action == 'on':
                appliance.turn_on()
                message = f"{appliance.name} turned on."
            elif action == 'off':
                appliance.turn_off()
                message = f"{appliance.name} turned off."
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': message, 'is_on': appliance.is_on})
        
        except Appliance.DoesNotExist:
            return Response({'error': 'Appliance not found'}, status=status.HTTP_404_NOT_FOUND)


class ApplianceEnergyUsageView(APIView):
    def get(self, request):
        appliance_list = Appliance.objects.all()

        total_power_usage = Appliance.objects.filter(is_on=True).aggregate(
            total=Sum('power_usage')
            )

        total_usage_value = total_power_usage['total'] or 0

        total_power_usage_serializer = PowerUsageSerializer(
            {'total_power_usage': total_usage_value}
            )
        appliance_list_serializer = ApplianceSerializer(
            appliance_list, many=True
            )

        data = {
            'total_power_usage': total_power_usage_serializer.data,
            'appliance_list': appliance_list_serializer.data
        }

        return Response(data)
