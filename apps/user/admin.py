from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from apps.user.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm
from apps.core.admin import ModelAdminBase
from apps.user.models import User


@admin.register(User)
class UserAdmin(ModelAdminBase):
    list_display = ("username", "is_active", "date_joined", "last_login")
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined",)}),
    )

    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username", "date_joined")
    list_filter = ("date_joined",)
    compressed_fields = True
    warn_unsaved_form = True
    filter_horizontal = ("groups", "user_permissions",)
    readonly_fields = ("last_login",)
    list_per_page = 20
    empty_value_display = "-empty-"


class TokenAdmin(ModelAdminBase):
    list_display = ("key", "user", "created")
    fields = ("user",)
    ordering = ("-created",)
    list_per_page = 20
    empty_value_display = "-empty-"


admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, TokenAdmin)
