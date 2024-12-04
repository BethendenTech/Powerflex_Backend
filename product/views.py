from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ApplianceCategory, Appliance
from .serializers import ApplianceCategorySerializer, ApplianceSerializer


@api_view(["GET"])
def appliance_category_list(request):
    categories = ApplianceCategory.objects.prefetch_related("appliances").all()
    serializer = ApplianceCategorySerializer(categories, many=True)
    return Response(serializer.data)
