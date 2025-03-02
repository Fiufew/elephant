from django.contrib import admin
from .models import CustomElephantUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomElephantUser)
class CustomElephantUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_employee', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Employee Information', {'fields': ('is_employee',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Employee Information', {'fields': ('is_employee',
                                             'is_superuser',
                                             'is_staff')}),
    )
