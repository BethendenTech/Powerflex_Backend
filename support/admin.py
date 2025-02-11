from django.contrib import admin
from .models import ContactForm

# Register your models here.


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone")
    list_filter = ("first_name", "last_name", "email", "phone")
    search_fields = ("first_name", "last_name", "email", "phone")
