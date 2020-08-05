from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.forms import (
    EmailInput,
    FileInput,
    ImageField,
    ModelForm,
    PasswordInput,
    TextInput,
)

from authentication.tasks import send_reset_password_email

from .constants import (
    ACCOUNT_FIELD_ATTRS,
    ACCOUNT_IMAGE_FIELD_ATTRS,
    CONFIRM_PASSWORD_ATTRS,
    EMAIL_ATTRS,
    NEW_PASSWORD_ATTRS,
    OLD_PASSWORD_ATTRS,
    PASSWORD_ATTRS,
    USERNAME_ATTRS,
)
from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = TextInput(attrs=USERNAME_ATTRS)
        self.fields["password"].widget = PasswordInput(attrs=PASSWORD_ATTRS)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = EmailInput(attrs=EMAIL_ATTRS)
        self.fields["username"].widget = TextInput(attrs=USERNAME_ATTRS)
        self.fields["password1"].widget = PasswordInput(attrs=PASSWORD_ATTRS)
        self.fields["password2"].widget = PasswordInput(
            attrs=CONFIRM_PASSWORD_ATTRS
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = EmailInput(attrs=EMAIL_ATTRS)

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        if not context.get("user"):
            return
        context["user"] = context["user"].id
        send_reset_password_email(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name,
        )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = PasswordInput(
            attrs=PASSWORD_ATTRS
        )
        self.fields["new_password2"].widget = PasswordInput(
            attrs=CONFIRM_PASSWORD_ATTRS
        )


class UpdateUserForm(ModelForm):
    image = ImageField(
        required=False, widget=FileInput(attrs=ACCOUNT_IMAGE_FIELD_ATTRS)
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": TextInput(attrs=ACCOUNT_FIELD_ATTRS),
            "email": EmailInput(attrs=ACCOUNT_FIELD_ATTRS),
        }


class CustomChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = PasswordInput(
            attrs=OLD_PASSWORD_ATTRS
        )
        self.fields["new_password1"].widget = PasswordInput(
            attrs=NEW_PASSWORD_ATTRS
        )
        self.fields["new_password2"].widget = PasswordInput(
            attrs=CONFIRM_PASSWORD_ATTRS
        )
