from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (("User", {"fields": ("name", "phone_number", "email")}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    ))
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ["email", "username", "phone_number", "name",]
    search_fields = ["name", "email",]

