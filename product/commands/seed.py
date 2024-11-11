from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Category, Product, Brand
import json

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        
        with open('backup/Category.json') as f:  # Update the path accordingly
            data = json.load(f)
            
        # Number of records to create
        number_of_records = data.length  # Adjust as needed

        for item in data.keys():
            Category.objects.create(
                name=item['name'],
                description=item['description'],
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {number_of_records} records into the database.'))
