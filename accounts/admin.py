from django.contrib import admin

from .models import AllowedSignupEmail, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_active", "is_staff", "is_superuser")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")


@admin.register(AllowedSignupEmail)
class AllowedSignupEmailAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_registered", "created_at")
    list_filter = ("role", "is_registered")
    search_fields = ("email",)
