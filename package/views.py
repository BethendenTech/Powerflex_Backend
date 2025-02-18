from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from product.utils import getPanel, getInverter, getBattery

from .models import Package, PackageOrder
from .serializers import (
    PackageSerializer,
    PackageOrderSerializer,
    PackageOrderViewSerializer,
    PackageOrderUpdateSerializer,
)
from setting.models import Settings


# Create your views here.
@api_view(["GET"])
def package_list(request):
    packages = Package.objects.prefetch_related("appliances", "package_products").all()
    serializer = PackageSerializer(packages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def package_detail(request, pk):
    package = Package.objects.prefetch_related("appliances", "package_products").get(
        pk=pk
    )
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

    best_inverter = getInverter(total_capacity)

    details.append(
        {
            "title": best_inverter[0]["inverter"],
            "quantity": best_inverter[0]["quantity"],
            "cost": best_inverter[0]["price"],
        }
    )

    best_battery = getBattery(total_capacity)

    details.append(
        {
            "title": best_battery[0]["battery"],
            "quantity": best_battery[0]["quantity"],
            "cost": best_battery[0]["price"],
        }
    )

    best_panel = getPanel(total_capacity)

    details.append(
        {
            "title": best_panel[0]["panel"],
            "quantity": best_panel[0]["quantity"],
            "cost": best_panel[0]["price"],
        }
    )

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


@api_view(["POST"])
def package_order(request):
    serializer = PackageOrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        if order:
            return Response(
                {"message": "Order created successfully", "order": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Failed to save order"}, status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def package_order_detail(request, pk):
    order = PackageOrder.objects.get(pk=pk)
    serializer = PackageOrderViewSerializer(order)
    return Response(serializer.data)


@api_view(["PUT"])
def package_order_update(request, pk):
    try:
        order = PackageOrder.objects.get(pk=pk)
    except PackageOrder.DoesNotExist:
        return Response(
            {"error": "PackageOrder not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = PackageOrderUpdateSerializer(
        order, data=request.data, partial=True
    )  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
