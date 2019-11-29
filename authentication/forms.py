from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
)
from django.forms import (
    ModelForm,
    TextInput,
    PasswordInput,
    EmailInput,
    EmailField,
    FileInput,
)
from django.conf import settings
from .constants import *
from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs=USERNAME_ATTRS)
        self.fields['password'].widget = PasswordInput(attrs=PASSWORD_ATTRS)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = EmailInput(attrs=EMAIL_ATTRS)
        self.fields['username'].widget = TextInput(attrs=USERNAME_ATTRS)
        self.fields['password1'].widget = PasswordInput(attrs=PASSWORD_ATTRS)
        self.fields['password2'].widget = PasswordInput(attrs=CONFIRM_PASSWORD_ATTRS)


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = EmailInput(attrs=EMAIL_ATTRS)


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget = PasswordInput(attrs=PASSWORD_ATTRS)
        self.fields['new_password2'].widget = PasswordInput(attrs=CONFIRM_PASSWORD_ATTRS)


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'image']
        widgets = {
            'username': TextInput(attrs=ACCOUNT_FIELD_ATTRS),
            'email': EmailInput(attrs=ACCOUNT_FIELD_ATTRS),
            'image': FileInput(attrs=ACCOUNT_IMAGE_FIELD_ATTRS)
        }


class CustomChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = PasswordInput(attrs=OLD_PASSWORD_ATTRS)
        self.fields['new_password1'].widget = PasswordInput(attrs=NEW_PASSWORD_ATTRS)
        self.fields['new_password2'].widget = PasswordInput(attrs=CONFIRM_PASSWORD_ATTRS)
