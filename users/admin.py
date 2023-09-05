from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    ordering = ['-date_joined']
    list_display = ('username', 'email', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'contact')
    list_filter = ('email', 'is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'contact')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),

    )
    
    add_fieldsets = (
        (None, {
            'classes': ('username', 'email', 'contact', 'password1', 'password2', 'date_joined', 'is_staff',
                       'is_superuser', 'is_active')
           }
        ),
    )
    
admin.site.register(User, UserAdminConfig)