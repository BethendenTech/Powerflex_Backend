from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Package
from .serializers import PackageSerializer


# Create your views here.
@api_view(["GET"])
def package_list(request):
    packages = Package.objects.prefetch_related("appliances").all()
    serializer = PackageSerializer(packages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def package_detail(request, pk):
    package = Package.objects.prefetch_related("appliances").get(pk=pk)
    serializer = PackageSerializer(package)
    return Response(serializer.data)
