from datetime import date
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


@api_view(["POST"])
def package_request(request):
    package_id = request.data.get("package_id")

    package = Package.objects.get(pk=package_id)

    total_capacity = 0

    for appliance in package.appliances.all():
        total_capacity += appliance.power_w

    details = []

    details.append({"title": "12kw Hybrid inverter", "quantity": 1, "cost": 100})
    details.append({"title": "10kw Lithium battery", "quantity": 1, "cost": 100})
    details.append({"title": "500W solar panel", "quantity": 1, "cost": 100})
    details.append({"title": "Accessories & Installation", "quantity": 1, "cost": 100})

    data = {
        "total_capacity": total_capacity,
        "total_cost": package.price,
        "details": details,
    }

    return Response(data)
