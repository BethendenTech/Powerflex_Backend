from product.models import Product, Appliance, Band


def getPanel(capacity):
    query = Product.objects.filter(category_id=1)
    panels = list(query)

    best_panel = []

    for panel in panels:
        panel_quantity = round(capacity / panel.capacity_w)
        panel_capacity = float(panel.capacity_w * panel_quantity)
        if panel_capacity >= capacity:
            best_panel.append(
                {
                    "panel": panel.name,
                    "price": float(panel.price_usd * panel_quantity),
                    "quantity": panel_quantity,
                    "capacity": panel_capacity,
                }
            )

    return best_panel


def getInverter(capacity):
    query = Product.objects.filter(category_id=2)
    inverters = list(query)

    best_inverter = []

    for inverter in inverters:
        inverter_quantity = round(capacity / inverter.capacity_w)
        inverter_capacity = float(inverter.capacity_w * inverter_quantity)
        if inverter_capacity >= capacity:
            best_inverter.append(
                {
                    "inverter": inverter.name,
                    "price": float(inverter.price_usd * inverter_quantity),
                    "quantity": inverter_quantity,
                    "capacity": inverter_capacity,
                }
            )

    return best_inverter


def getBattery(capacity):
    query = Product.objects.filter(category_id=3)
    batteries = list(query)

    best_battery = []

    for battery in batteries:
        battery_quantity = round(capacity / battery.capacity_w)
        battery_capacity = float(battery.capacity_w * battery_quantity)
        if battery_capacity >= capacity:
            best_battery.append(
                {
                    "battery": battery.name,
                    "price": float(battery.price_usd * battery_quantity),
                    "quantity": battery_quantity,
                    "capacity": battery_capacity,
                }
            )

    return best_battery
