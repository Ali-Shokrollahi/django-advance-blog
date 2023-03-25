from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "is_active", "is_staff")
    list_filter = ("created", "is_staff", "is_active",)
    ordering = ("-created",)
    search_fields = ("email",)

    fieldsets = (
        ('Dates', {'fields': ('created', 'modified', 'last_login')}),
        ('Authentication', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'email_verified')}),
        ('Group and Permissions', {'fields': ('groups', 'user_permissions')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active')}
         ),
    )
    readonly_fields = ('created', 'modified')


admin.site.register(User, UserAdmin)
