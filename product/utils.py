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
                    "price": float(panel.price_usd*panel_quantity),
                    "quantity": panel_quantity,
                    "capacity": panel_capacity,
                }
            )

    return best_panel
