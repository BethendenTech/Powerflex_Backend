from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ApplianceCategory, Band
from .serializers import ApplianceCategorySerializer, BandSerializer


@api_view(["GET"])
def appliance_category_list(request):
    categories = ApplianceCategory.objects.prefetch_related("appliances").all()
    serializer = ApplianceCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def band_list(request):
    bands = Band.objects.all()
    serializer = BandSerializer(bands, many=True)
    return Response(serializer.data)
