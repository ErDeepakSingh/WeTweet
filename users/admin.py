from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django.db import models
from .models import User,Profile,FollowUser


class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ('email', 'username')
    list_filter = ('email', 'username',  'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'username',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
        # ('Personal', {'fields': ()}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(FollowUser)