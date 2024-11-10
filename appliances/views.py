from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appliance
from .serializers import ApplianceSerializer, PowerUsageSerializer
from django.db.models import Sum

class ApplianceToggleView(APIView):
    def post(self, request):
        appliance_ids = request.data.get('appliance_ids', [])
        action = request.data.get('action')

        if not appliance_ids or not action:
            return Response({'error': 'Missing appliance_ids or action'}, status=status.HTTP_400_BAD_REQUEST)

        appliances = Appliance.objects.filter(id__in=appliance_ids)
        if not appliances.exists():
            return Response({'error': 'One or more appliances not found'}, status=status.HTTP_404_NOT_FOUND)

        messages = []
        for appliance in appliances:
            if action == 'on':
                appliance.turn_on()
                messages.append(f"{appliance.name} turned on.")
            elif action == 'off':
                appliance.turn_off()
                messages.append(f"{appliance.name} turned off.")
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplianceSerializer(appliances, many=True)
        return Response({'messages': messages, 'appliances': serializer.data})


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
