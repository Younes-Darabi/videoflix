from django.contrib import admin
from .models import CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['email']
    ordering = ['-date_joined']

admin.site.register(CustomUser, UserAdmin)