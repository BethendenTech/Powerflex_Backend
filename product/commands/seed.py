import json
from django.core.management.base import BaseCommand
from ..models import Category, Brand, Product

class Command(BaseCommand):
    help = 'Seed the database with categories, brands, and products'

    def handle(self, *args, **kwargs):
        # Sample data for categories
        categories_data = [
            {"name": "Solar Panels", "description": "Various types of solar panels."},
            {"name": "Inverters", "description": "Devices to convert DC to AC."},
            {"name": "Batteries", "description": "Energy storage solutions."},
        ]

        # Sample data for brands
        brands_data = [
            {"name": "SunPower", "description": "Leading solar technology company."},
            {"name": "Gospower", "description": "Reliable power solutions."},
            {"name": "tbc", "description": "To be confirmed."},
        ]

        # Sample data for products
        products_data = [
            {
                "category": "Solar Panels",
                "brand": "tbc",
                "name": "350W Mono Panel",
                "unique_code": "SP350W2023",
                "model_name": "tbc",
                "model_year": None,
                "country_of_origin": "tbc",
                "capacity_w": 350,
                "price_usd": 46.53,
                "voc_v": None,
                "isc_a": None,
                "efficiency": 90,
                "phase_type": None,
                "warranty_years": None,
                "voltage": None,
                "dod": None,
                "cycle_life": None,
            },
            {
                "category": "Solar Panels",
                "brand": "tbc",
                "name": "420W Half-Cut Panel",
                "unique_code": "SP420W2023",
                "model_name": "tbc",
                "model_year": None,
                "country_of_origin": "tbc",
                "capacity_w": 420,
                "price_usd": 59.13,
                "voc_v": None,
                "isc_a": None,
                "efficiency": 90,
                "phase_type": None,
                "warranty_years": None,
                "voltage": None,
                "dod": None,
                "cycle_life": None,
            },
            {
                "category": "Solar Panels",
                "brand": "SunPower",
                "name": "500W Half-Cut Panel",
                "unique_code": "SP500W2023",
                "model_name": "HalfCut500",
                "model_year": 2023,
                "country_of_origin": "USA",
                "capacity_w": 500,
                "price_usd": 73.01,
                "voc_v": 50.2,
                "isc_a": 10.5,
                "efficiency": 90,
                "phase_type": None,
                "warranty_years": None,
                "voltage": None,
                "dod": None,
                "cycle_life": None,
            },
            {
                "category": "Inverters",
                "brand": "Gospower",
                "name": "6kW Inverter",
                "unique_code": "INV6KW2023",
                "model_name": "GPEX-6KL1",
                "model_year": None,
                "country_of_origin": "China",
                "capacity_w": 6000,
                "price_usd": 302.66,
                "voc_v": None,
                "isc_a": None,
                "efficiency": 90,
                "phase_type": "Single Phase",
                "warranty_years": 5,
                "voltage": 230,
                "dod": None,
                "cycle_life": None,
            },
            {
                "category": "Batteries",
                "brand": "Gospower",
                "name": "10kWh Lithium Battery",
                "unique_code": "GPLB-48200M-2024",
                "model_name": "GPLB-48200M",
                "model_year": 2024,
                "country_of_origin": "China",
                "capacity_w": None,
                "price_usd": 1560.69,
                "voc_v": None,
                "isc_a": None,
                "efficiency": 98,
                "phase_type": None,
                "warranty_years": None,
                "voltage": 51.2,
                "dod": 80,
                "cycle_life": 5000,
            },
        ]

        # Create categories
        categories = {}
        for category in categories_data:
            cat = Category.objects.create(**category)
            categories[cat.name] = cat

        # Create brands
        brands = {}
        for brand in brands_data:
            br = Brand.objects.create(**brand)
            brands[br.name] = br

        # Create products
        for product in products_data:
            category = categories[product.pop("category")]
            brand = brands[product.pop("brand")]
            Product.objects.create(category=category, brand=brand, **product)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
