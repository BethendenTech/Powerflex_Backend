from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.utils import getPanel
from .models import Package
from .serializers import PackageSerializer
from setting.models import Settings


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

    systemSetting = Settings.objects.first()

    total_capacity = 0
    package_cost = package.price
    total_cost = package.price

    for appliance in package.appliances.all():
        total_capacity += appliance.power_w

    details = []

    details.append({"title": "12kw Hybrid inverter", "quantity": 1, "cost": 100})
    details.append({"title": "10kw Lithium battery", "quantity": 1, "cost": 100})

    best_panel = getPanel(total_capacity)
    print("best_panel", best_panel[0]["panel"])

    details.append({"title": best_panel[0]["panel"], "quantity": best_panel[0]["quantity"], "cost": best_panel[0]["price"]})

    if systemSetting and systemSetting.installation_margin is not None:
        installation_margin = float(systemSetting.installation_margin)
    else:
        installation_margin = 0

    installation_margin_cost = float(float(total_cost) * installation_margin) / 100
    total_cost = float(float(total_cost) + installation_margin_cost)

    details.append(
        {
            "title": "Accessories & Installation",
            "quantity": 1,
            "cost": installation_margin_cost,
        }
    )

    data = {
        "total_capacity": total_capacity,
        "package_cost": package_cost,
        "total_cost": total_cost,
        "details": details,
    }

    return Response(data)
