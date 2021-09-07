from django.contrib import admin

from app_users.models import Profile, UserStatus


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'scores_needed']
