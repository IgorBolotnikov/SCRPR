from django.urls import path

from .views import (
    ChangePasswordDoneView,
    ChangePasswordView,
    CompleteResetPasswordView,
    CustomLoginView,
    DeleteAccountView,
    EditAccountView,
    RegisterView,
    ResetPasswordRequestDoneView,
    ResetPasswordRequestView,
    ResetPasswordView,
)

app_name = "authentication"
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path(
        "reset_password",
        ResetPasswordRequestView.as_view(),
        name="reset_request",
    ),
    path(
        "reset_password/<str:uidb64>/<str:token>",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
    path(
        "reset_password_done",
        ResetPasswordRequestDoneView.as_view(),
        name="reset_password_done",
    ),
    path(
        "reset_password_complete",
        CompleteResetPasswordView.as_view(),
        name="reset_password_complete",
    ),
    path(
        "change_password", ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "change_password_done",
        ChangePasswordDoneView.as_view(),
        name="change_password_done",
    ),
    path(
        "delete_account/<int:pk>",
        DeleteAccountView.as_view(),
        name="delete_account",
    ),
    path(
        "edit_account/<int:pk>", EditAccountView.as_view(), name="edit_account"
    ),
]
