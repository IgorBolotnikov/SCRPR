from pathlib import Path

from django.utils.translation import gettext_lazy as _

USER_EMAIL_CONSTRAINT_MESSAGE = _("A user with that email already exists.")

LOGIN_TITLE = _("Login")
REGISTER_TITLE = _("Register")
REGISTER_SUCCESS_MESSAGE = _("Registration is successful! Now you can login.")

RESET_PASSWORD_TITLE = _("Reset Password")

USERNAME_ATTRS = {"class": "auth_field field", "placeholder": _("Username")}
EMAIL_ATTRS = {"class": "auth_field field", "placeholder": _("Email")}
PASSWORD_ATTRS = {"class": "auth_field field", "placeholder": _("Password")}
OLD_PASSWORD_ATTRS = {
    "class": "auth_field field",
    "placeholder": _("Old Password"),
}
NEW_PASSWORD_ATTRS = {
    "class": "auth_field field",
    "placeholder": _("New Password"),
}
CONFIRM_PASSWORD_ATTRS = {
    "class": "auth_field field",
    "placeholder": _("Confirm password"),
}

ACCOUNT_FIELD_ATTRS = {
    "class": "field auth_field",
}
ACCOUNT_IMAGE_FIELD_ATTRS = {
    "class": "account_image_field",
}

USER_IMAGE_SIZE = (120, 120)
with open(Path(__file__).parent / "authentication" / "image.txt") as fd:
    DEFAULT_USER_IMAGE = fd.read().strip()
