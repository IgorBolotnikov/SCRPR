from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreateForm(UserCreationForm):

    class Meta:
        model=User
        fields=('username', 'email', 'first_name', 'last_name', 'image')


class UserUpdateForm(UserChangeForm):

    class Meta:
        model=User
        fields=(
            'username',
            'email',
            'first_name',
            'last_name',
            'image',
            'slug',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'last_login',
            'date_joined'
        )


class UserAdmin(BaseUserAdmin):
    form = UserUpdateForm
    add_form = UserCreateForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'image', 'slug')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email','first_name', 'last_name', 'image', 'password1', 'password2')}
        ),
    )

admin.site.register(User, UserAdmin)
