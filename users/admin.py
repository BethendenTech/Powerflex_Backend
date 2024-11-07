from django.contrib import admin
from .models import UserDetail

# Register your models here.

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','phone_number') 
    search_fields = ('name',)
    list_filter = ('email',)
    ordering = ('name',)
