import json
import os
from django.core.management.base import BaseCommand
from cms.models import FAQ

class Command(BaseCommand):
    help = 'Exports FAQs to a fixture file in the cms/fixtures directory'

    def handle(self, *args, **kwargs):
        # Define output file path
        output_dir = 'cms/fixtures'
        output_file = os.path.join(output_dir, 'faq_fixture.json')

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Get all FAQ objects
        faqs = FAQ.objects.all().values('id', 'name', 'description')

        # Custom debug print
        self.stdout.write(f"Process lines, file_name command_line {output_file.encode('utf-8')}")

        # Serialize the data using json.dumps with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(list(faqs), f, ensure_ascii=False, indent=4)

        # Confirmation message
        self.stdout.write(f"FAQs successfully exported to {output_file}")
