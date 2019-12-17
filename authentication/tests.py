import tempfile
from django.core import mail
from django.urls import reverse
from django.test import TestCase, SimpleTestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from .views import *
from .models import *


# Virtual image file to test proper user image formatting and saving
IMAGE_MOCK = tempfile.NamedTemporaryFile(suffix=".jpg").name
PDF_FILE_MOCK = tempfile.NamedTemporaryFile(suffix=".pdf").name


# ===== Always present templates =====

BASE_TEMPLATE = 'authentication/base.html'
NAVBAR_TEMPLATE = 'authentication/navbar.html'
FOOTER_TEMPLATE = 'authentication/footer.html'


# ===== Field errors =====

# Errors for checking User fields size and type validations
USERNAME_ERROR_1 = 'Ensure this value has at most 150 characters (it has 151).'
EMAIL_ERROR_1 = 'Enter a valid email address.'
# Errors for checking User fields uniqueness validations
USERNAME_ERROR_2 = 'A user with that username already exists.'
EMAIL_ERROR_2 = 'A user with that email already exists.'
CONFIRM_PASSWORD_ERROR_1 = "The two password fields didn't match."
CONFIRM_PASSWORD_ERRORS_2 = [
    'This password is too short. It must contain at least 8 characters.',
    'This password is too common.',
    'This password is entirely numeric.'
]
LOGIN_ERROR = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'


# ===== Test forms (valid, invalid, form errors) =====

# Valid forms
LOGIN_VALID_FORM_SAMPLE = {
    'username': 'TestUser1',
    'password': 'testuser1password'
}
REGISTER_VALID_FORM_SAMPLE = {
    'email': 'testuser3@testemail.com',
    'username': 'TestUser3',
    'password1': 'testuser3password',
    'password2': 'testuser3password'
}
RESET_PASSWORD_REQUEST_VALID_FORM = {
    'email': 'testuser1@testemail.com'
}
RESET_PASSWORD_VALID_FORM = {
    'new_password1': 'newsecretpassword',
    'new_password2': 'newsecretpassword'
}
CHANGE_PASSWORD_VALID_FORM = {
    'old_password': 'testuser1password',
    'new_password1': 'newsecretpassword',
    'new_password2': 'newsecretpassword'
}
EDIT_USER_VALID_FORM = {
    'username': 'NewTestUser',
    'email': 'newtestuseremail@testemail.com',
    'image': IMAGE_MOCK
}

# Invalid forms
LOGIN_INVALID_FORM_SAMPLE_1 = {
    'username': 'NotRegisteredUsername',
    'password': 'wrong-password',
}
LOGIN_INVALID_FORM_SAMPLE_2 = {
    'username': 'TestUser1',
    'password': 'wrong-password',
}
REGISTER_INVALID_FORM_SAMPLE_1 = {
    'email': ''.join(['q' for q in range(151)]),
    'username': ''.join(['q' for q in range(151)]),
    'password1': '111111',
    'password2': '222222'
}
REGISTER_FORM_ERRORS_1 = {
    'email': EMAIL_ERROR_1,
    'username': USERNAME_ERROR_1,
    'password1': None,
    'password2': CONFIRM_PASSWORD_ERROR_1
}
REGISTER_INVALID_FORM_SAMPLE_2 = {
    # These credentials were already used when setting up database
    'email': 'testuser1@testemail.com',
    'username': 'TestUser1',
    'password1': '111111',
    'password2': '111111'
}
REGISTER_FORM_ERRORS_2 = {
    'email': EMAIL_ERROR_2,
    'username': USERNAME_ERROR_2,
    'password1': None,
    'password2': CONFIRM_PASSWORD_ERRORS_2
}
RESET_PASSWORD_REQUEST_INVALID_FORM_1 = {
    'email': 'notavalidemail'
}
RESET_PASSWORD_REQUEST_INVALID_ERRORS_1 = {
    'email': EMAIL_ERROR_1
}
CHANGE_PASSWORD_INVALID_FORM = {
    'old_password': 'invalidpassword',
    'new_password1': 'newsecretpassword',
    'new_password2': 'newsecretpassword'
}
CHANGE_PASSWORD_ERRORS = {
    'old_password': None,
    'new_password1': None,
    'new_password2': None
}
EDIT_ACCOUNT_INVALID_FORM_1 = {
    'username': ''.join(['q' for q in range(151)]),
    'email': ''.join(['q' for q in range(151)]),
    'image': PDF_FILE_MOCK,
}
EDIT_ACCOUNT_ERRORS_1 = {
    'email': EMAIL_ERROR_1,
    'username': USERNAME_ERROR_1,
    'image': None
}
EDIT_ACCOUNT_INVALID_FORM_2 = {
    'email': 'testuser2@testemail.com',
    'username': 'TestUser2',
    'image': PDF_FILE_MOCK,
}
EDIT_ACCOUNT_ERRORS_2 = {
    'email': EMAIL_ERROR_2,
    'username': USERNAME_ERROR_2,
    'image': None
}


# Mixins for testing separate features

class TestGetResponseMixin:
    def test_get_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        if hasattr(self, 'template_base'):
            self.assertTemplateUsed(self.template_base)
        self.assertTemplateUsed(BASE_TEMPLATE)
        self.assertTemplateUsed(NAVBAR_TEMPLATE)
        self.assertTemplateUsed(FOOTER_TEMPLATE)


class TestFormValidationMixin:
    def test_form_fields_validation_errors(self):
        for form_sample, form_errors in zip(self.invalid_form_samples,
                                            self.invalid_form_errors):
            response = self.client.post(self.url, form_sample)
            for field_name in form_sample.keys():
                self.assertFormError(
                    response, 'form', field_name, form_errors[field_name])


class TestObjectDeletionWithRedirectMixin:
    def test_object_deletion_with_redirect(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, self.redirect_url)
        deleted_object = self.model.objects.filter(pk=1).first()
        self.assertEqual(deleted_object, None)


class TestModelInstancesContextMixin:
    def test_model_instances_context(self):
        test_objects = [repr(object) for object in self.model.objects.all()]
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['object_list'],
            test_objects,
            ordered=False
        )

# Test for prepopulating database

class TestCaseWithDatabase(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create(
            email = 'testuser1@testemail.com',
            username = 'TestUser1',
        )
        test_user2 = User.objects.create(
            email = 'testuser2@testemail.com',
            username = 'TestUser2'
        )
        test_user1.set_password('testuser1password')
        test_user2.set_password('testuser2password')
        test_user1.save()
        test_user2.save()

    def test_user_passwords(self):
        test_user1 = User.objects.get(pk=1)
        test_user2 = User.objects.get(pk=2)
        self.assertTrue(test_user1.password is not None)
        self.assertTrue(test_user2.password is not None)


class TestLoginView(TestCaseWithDatabase,
                    TestGetResponseMixin):
    def setUp(self):
        self.url = '/auth/login'
        self.template_name = 'authentication/login.html'
        self.redirect_url = '/'
        self.invalid_form_samples = (
            LOGIN_INVALID_FORM_SAMPLE_1,
            LOGIN_INVALID_FORM_SAMPLE_2
        )
        self.valid_form_sample = LOGIN_VALID_FORM_SAMPLE

    def test_failed_login_attempt(self):
        for form_sample in self.invalid_form_samples:
            response = self.client.post(self.url, form_sample)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['form'].errors['__all__'][0],
                LOGIN_ERROR
            )

    def test_valid_login_attempt(self):
        response = self.client.post(self.url, self.valid_form_sample)
        self.assertRedirects(response, self.redirect_url)


class TestRegisterView(TestCaseWithDatabase,
                       TestGetResponseMixin,
                       TestFormValidationMixin):
    def setUp(self):
        self.url = '/auth/register'
        self.template_name = 'authentication/register.html'
        self.redirect_url = '/auth/login'
        self.invalid_form_samples = (
            REGISTER_INVALID_FORM_SAMPLE_1,
            REGISTER_INVALID_FORM_SAMPLE_2
        )
        self.invalid_form_errors = (
            REGISTER_FORM_ERRORS_1,
            REGISTER_FORM_ERRORS_2
        )
        self.valid_form_sample = REGISTER_VALID_FORM_SAMPLE

    def test_user_creation(self):
        response = self.client.post(self.url, self.valid_form_sample)
        object = User.objects.filter(pk=3).first()
        self.assertEqual(object.username, self.valid_form_sample['username'])
        self.assertEqual(object.email, self.valid_form_sample['email'])
        self.assertTrue(object.image is not None)


class TestResetPasswordRequestView(TestCaseWithDatabase,
                                   TestGetResponseMixin,
                                   TestFormValidationMixin):
    def setUp(self):
        self.url = '/auth/reset_password'
        self.template_name = 'authentication/reset_request.html'
        self.success_url = '/auth/reset_password_done'
        self.invalid_form_samples = (RESET_PASSWORD_REQUEST_INVALID_FORM_1,)
        self.invalid_form_errors = (RESET_PASSWORD_REQUEST_INVALID_ERRORS_1,)
        self.valid_form_sample = RESET_PASSWORD_REQUEST_VALID_FORM

    def test_correct_email_entry(self):
        response = self.client.post(self.url, self.valid_form_sample)
        self.assertRedirects(response, self.success_url)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reset password message')


class TestResetPasswordRequestDoneView(TestCaseWithDatabase,
                                       TestGetResponseMixin):
    def setUp(self):
        self.url = '/auth/reset_password_done'
        self.template_name = 'authentication/reset_password_done.html'


class TestResetPasswordView(TestCaseWithDatabase,
                            TestGetResponseMixin):
    def setUp(self):
        self.url = ''
        self.template_name = 'authentication/reset_password.html'
        self.success_url = '/auth/reset_password_complete'
        self.valid_form_sample = RESET_PASSWORD_VALID_FORM

    def test_get_response(self):
        response = self.client.post(
            '/auth/reset_password',
            RESET_PASSWORD_REQUEST_VALID_FORM
        )
        uid = response.context[0]['uid']
        token = response.context[0]['token']
        self.url = f'/auth/reset_password/{uid}/set-password'
        return super().test_get_response()

    # TODO: create test for resetting password and checking new password


class TestChangePasswordView(TestCaseWithDatabase,
                             TestGetResponseMixin,
                             TestFormValidationMixin):
    def setUp(self):
        self.url = '/auth/change_password'
        self.template_name = 'authentication/change_password.html'
        self.success_url = '/auth/change_password_done'
        self.client.login(
            username='TestUser1',
            password='testuser1password'
        )
        self.invalid_form_samples = (CHANGE_PASSWORD_INVALID_FORM,)
        self.invalid_form_errors = (CHANGE_PASSWORD_ERRORS,)
        self.valid_form_sample = CHANGE_PASSWORD_VALID_FORM

    def test_change_password(self):
        response = self.client.post(self.url, self.valid_form_sample)
        self.assertRedirects(response, self.success_url)
        user = User.objects.get(pk=1)
        self.assertTrue(user.check_password('newsecretpassword'))


class CompleteResetPasswordView(TestCaseWithDatabase,
                                TestGetResponseMixin):
    def setUp(self):
        self.url = '/auth/reset_password_complete'
        self.template_name = 'authentication/reset_password_complete.html'


class TestDeleteAccountView(TestCaseWithDatabase,
                            TestGetResponseMixin,
                            TestObjectDeletionWithRedirectMixin):
    def setUp(self):
        self.url = '/auth/delete_account/1'
        self.template_name = 'authentication/delete_account.html'
        self.redirect_url = '/auth/register'
        self.model = User
        self.client.login(
            username = 'TestUser1',
            password = 'testuser1password'
        )


class TestEditAccountView(TestCaseWithDatabase,
                          TestGetResponseMixin,
                          TestFormValidationMixin):
    def setUp(self):
        self.url = '/auth/edit_account/1'
        self.template_name = 'authentication/edit_account.html'
        self.success_url = '/favorites'
        self.invalid_form_samples = (
            EDIT_ACCOUNT_INVALID_FORM_1,
            EDIT_ACCOUNT_INVALID_FORM_2
        )
        self.invalid_form_errors = (
            EDIT_ACCOUNT_ERRORS_1,
            EDIT_ACCOUNT_ERRORS_2
        )
        self.valid_form_sample = EDIT_USER_VALID_FORM
        self.client.login(
            username = 'TestUser1',
            password = 'testuser1password'
        )

    def test_successfull_user_edit(self):
        response = self.client.post(self.url, self.valid_form_sample)
        self.assertRedirects(response, self.success_url)
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, 'NewTestUser')
        self.assertEqual(user.email, 'newtestuseremail@testemail.com')
        self.assertEqual(type(user.image), str)
