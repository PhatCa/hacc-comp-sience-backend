from django.urls import path
from .views import ApplianceToggleView, ApplianceEnergyUsageView

urlpatterns = [
    path('appliances/toggle/', ApplianceToggleView.as_view(), name='appliance-toggle'),
    path('appliances/energy-usage/', ApplianceEnergyUsageView.as_view(), name='appliance-energy-usage'),
]