import io
from base64 import b64encode

from PIL import Image

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView

from .constants import (
    LOGIN_TITLE,
    REGISTER_SUCCESS_MESSAGE,
    REGISTER_TITLE,
    RESET_PASSWORD_TITLE,
    USER_IMAGE_SIZE,
)
from .forms import (
    CustomChangePasswordForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    LoginForm,
    RegisterForm,
    UpdateUserForm,
)
from .models import User


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = LOGIN_TITLE
        return context

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR, form.errors["__all__"][0]
        )
        return super().form_invalid(form)


class RegisterView(FormView):
    template_name = "authentication/register.html"
    success_url = "/auth/login/?next="
    form_class = RegisterForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = REGISTER_TITLE
        return context

    @never_cache
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = RegisterForm(request.POST)
        context["form"] = form
        if form.is_valid():
            user = User(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
            )
            user.set_password(form.cleaned_data["password1"])
            user.save()
            next_url = request.GET.get("next")
            self.success_url += (
                next_url if next_url else settings.LOGIN_REDIRECT_URL
            )
            messages.add_message(
                request, messages.SUCCESS, REGISTER_SUCCESS_MESSAGE
            )
            return redirect(self.success_url, context, *args, **kwargs)
        return render(request, self.template_name, context)


class ResetPasswordRequestView(PasswordResetView):
    template_name = "authentication/reset_request.html"
    success_url = "/auth/reset_password_done"
    model = User
    form_class = CustomPasswordResetForm
    email_template_name = "authentication/reset_password_message.html"
    html_email_template_name = "authentication/reset_password_message.html"
    subject_template_name = "authentication/reset_password_subject.txt"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = RESET_PASSWORD_TITLE
        return context


class ResetPasswordRequestDoneView(PasswordResetDoneView):
    template_name = "authentication/reset_password_done.html"


class ResetPasswordView(PasswordResetConfirmView):
    template_name = "authentication/reset_password.html"
    success_url = "/auth/reset_password_complete"
    form_class = CustomSetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = RESET_PASSWORD_TITLE
        return context


class CompleteResetPasswordView(PasswordResetCompleteView):
    template_name = "authentication/reset_password_complete.html"


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "authentication/change_password.html"
    login_url = "/auth/login/"
    model = User
    form_class = CustomChangePasswordForm
    success_url = "/auth/change_password_done"


class ChangePasswordDoneView(LoginRequiredMixin, TemplateView):
    template_name = "authentication/change_password_done.html"
    login_url = "/auth/login/"


class DeleteAccountView(DeleteView):
    template_name = "authentication/delete_account.html"
    twmplate_name_suffix = ""
    model = User
    success_url = "/auth/register"
    context_object_name = "account"


class EditAccountView(LoginRequiredMixin, UpdateView):
    template_name = "authentication/edit_account.html"
    model = User
    form_class = UpdateUserForm
    success_url = "/favorites"
    login_url = "/auth/login/"
    context_object_name = "account"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Account"
        return context

    def form_valid(self, form):
        image = self.request.FILES.get("image")
        if image:
            image = self.get_encoded_image(image)
            self.object.image = image
        return super().form_valid(form)

    @staticmethod
    def get_encoded_image(image):
        image = Image.open(image)
        image.resize(USER_IMAGE_SIZE)
        filepath = io.BytesIO()
        image.save(filepath, image.format)
        image_binary = filepath.getvalue()
        image_string = b64encode(image_binary).decode("utf-8")
        return f"data:image/jpeg;base64,{image_string}"
