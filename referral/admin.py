from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'invite_code', 'used_invite_code', 'is_verified']
    search_fields = ['phone_number', 'invite_code']
