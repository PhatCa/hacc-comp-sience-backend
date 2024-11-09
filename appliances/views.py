from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appliance
from .serializers import ApplianceSerializer

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
        appliance_ids = request.query_params.getlist('appliance_ids')

        if not appliance_ids:
            return Response({'error': 'Missing appliance_ids'}, status=status.HTTP_400_BAD_REQUEST)

        appliances = Appliance.objects.filter(id__in=appliance_ids)
        if not appliances.exists():
            return Response({'error': 'One or more appliances not found'}, status=status.HTTP_404_NOT_FOUND)

        appliance_data = []
        for appliance in appliances:
            serializer = ApplianceSerializer(appliance)
            energy_usage = appliance.power_usage if appliance.is_on else 0.0
            appliance_data.append({
                'appliance': serializer.data,
                'energy_used': energy_usage
            })

        return Response({'appliances': appliance_data})