from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from django.db import models
from django.test import TestCase

from authentication.models import User
from scrpr.models import Comment, FavoriteGameQuery, FavoriteJobQuery, NewsPost

pytestmark = pytest.mark.django_db

LOGIN_URL = "/auth/login/?next="

# ===== Always present templates =====

BASE_TEMPLATE = "scrpr/base.html"
NAVBAR_TEMPLATE = "scrpr/navbar.html"
FOOTER_TEMPLATE = "scrpr/footer.html"

NAVBAR_USER_LINKS = ("Log Out", "My Account")
NAVBAR_NOUSER_LINKS = ("Log In", "Register")


# ===== Forms (valid, invalid, errors) =====

# Valid forms
RATE_VALID_FORM = {"name": "TestName", "comment": "Test Comment"}

# Invalid forms and form errors
RATE_INVALID_FORM = {
    "name": "".join(["q" for q in range(101)]),
    "comment": "Anyway valid comment",
}
RATE_ERRORS = {
    "name": "Ensure this value has at most 100 characters (it has 101).",
    "comment": None,
}


class GetResponseMixin:
    url: str
    template_name: str

    def test_get_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        if hasattr(self, "template_base"):
            self.assertTemplateUsed(self.template_base)
        self.assertTemplateUsed(BASE_TEMPLATE)
        self.assertTemplateUsed(NAVBAR_TEMPLATE)
        self.assertTemplateUsed(FOOTER_TEMPLATE)


class FormValidationMixin:
    invalid_form_samples: tuple
    invalid_form_errors: tuple
    url: str

    def test_form_fields_validation_errors(self):
        for form_sample, form_errors in zip(
            self.invalid_form_samples, self.invalid_form_errors
        ):
            response = self.client.post(self.url, form_sample)
            for field_name in form_sample.keys():
                self.assertFormError(
                    response, "form", field_name, form_errors[field_name]
                )


class ObjectDeletionWithRedirectMixin:
    url: str
    redirect_url: str
    model: models.Model

    def test_object_deletion_with_redirect(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, self.redirect_url)
        deleted_object = self.model.objects.filter(pk=1).first()
        self.assertEqual(deleted_object, None)


class ModelInstancesContextMixin:
    url: str
    model: models.Model

    def test_model_instances_context(self):
        test_objects = [repr(obj) for obj in self.model.objects.all()]
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context["object_list"], test_objects, ordered=False
        )


class SingleObjectContextMixin:
    url: str
    model: models.Model

    def test_object_context(self):
        test_object = self.model.objects.get(pk=1)
        response = self.client.get(self.url)
        self.assertEqual(response.context["object"].id, 1)
        self.assertEqual(response.context["object"], test_object)


class RedirectIfNoUserMixin:
    url: str
    next: str

    def test_redirect_if_no_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, LOGIN_URL + self.next)


class RedirectIfWrongUserMixin:
    url: str

    def test_redirect_if_wrong_user(self):
        self.client.login(username="TestUser2", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class WebScrapingResultsMixin:
    url: str
    queries: list

    def test_scraping_results_with_var_queries(self):
        # Create mock scrapers to avoid realtime web scraping from websites
        game_patcher = patch("scrpr.views.PSStoreScraper")
        game_mock = game_patcher.start()
        game_mock = game_mock()
        game_mock.scrape_game_website.return_value = {
            "object_list": ["result1", "result2"],
            "last_page": 1,
        }

        job_patcher = patch("scrpr.views.JobsSitesScraper")
        job_mock = job_patcher.start()
        job_mock = job_mock()
        job_mock.scrape_websites.return_value = {
            "object_list": ["result1", "result2"],
            "last_page": 1,
        }

        response = self.client.get(self.url)
        self.assertTrue(
            len(response.context["object_list"]) > 0,
            f'Web search from URL "{self.url} did not return any results"',
        )
        for query in self.queries:
            url = self.url + query
            response = self.client.get(url)
            self.assertTrue(
                response.context["object_list"] is not None,
                f'Web search from URL "{url} did not return results list"',
            )


class TestMainPageView(TestCase, GetResponseMixin):
    def setUp(self):
        self.url = ""
        self.template_name = "scrpr/index.html"


class TestNewsListView(TestCase, GetResponseMixin, ModelInstancesContextMixin):
    @classmethod
    def setUpTestData(cls):
        NewsPost.objects.create(
            title="Test1",
            body="<p>Test Body1</p>",
            datetime_posted=datetime.now(timezone.utc),
        )
        NewsPost.objects.create(
            title="Test2",
            body="<p>Test Body2</p>",
            datetime_posted=datetime.now(timezone.utc),
        )

    def setUp(self):
        self.url = "/news"
        self.template_name = "scrpr/news.html"
        self.model = NewsPost


class TestFavoritesView(TestCase, GetResponseMixin, RedirectIfNoUserMixin):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="TestUser1", email="testuser1@testemail.com"
        )
        user.set_password("testpassword")
        user.save()
        FavoriteGameQuery.objects.create(
            title="TestName", free=True, account=user
        )
        FavoriteJobQuery.objects.create(title="Test title", account=user)

    def setUp(self):
        self.url = "/favorites"
        self.template_name = "scrpr/content_with_sidebar/favorites.html"
        self.template_base = (
            "scrpr/content_with_sidebar/content_with_sidebar_base.html"
        )
        self.client.login(username="TestUser1", password="testpassword")
        self.games_model = FavoriteGameQuery
        self.jobs_model = FavoriteJobQuery
        self.next = "/favorites"

    def test_games_favorites_context(self):
        test_objects = [
            repr(object) for object in self.games_model.objects.all()
        ]
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context["object_list_games"], test_objects, ordered=False
        )

    def test_jobs_favorites_context(self):
        test_objects = [
            repr(object) for object in self.jobs_model.objects.all()
        ]
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context["object_list_jobs"], test_objects, ordered=False
        )


class TestFavoritesGameDetailView(
    TestCase,
    GetResponseMixin,
    RedirectIfNoUserMixin,
    RedirectIfWrongUserMixin,
    SingleObjectContextMixin,
):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username="TestUser1", email="testuser1@testemail.com"
        )
        user2 = User.objects.create(
            username="TestUser2", email="testuser2@testemail.com"
        )
        user1.set_password("testpassword")
        user2.set_password("testpassword")
        user1.save()
        user2.save()
        FavoriteGameQuery.objects.create(
            title="TestName", free=True, account=user1
        )
        FavoriteGameQuery.objects.create(
            title="TestName", free=True, account=user2
        )
        FavoriteJobQuery.objects.create(title="Test title", account=user1)

    def setUp(self):
        self.url = "/favorites/games/1"
        self.template_name = "scrpr/content_with_sidebar/favorites_game.html"
        self.template_base = (
            "scrpr/content_with_sidebar/content_with_sidebar_base.html"
        )
        self.model = FavoriteGameQuery
        self.client.login(username="TestUser1", password="testpassword")
        self.next = "/favorites/games/1"
        self.success_url = "/favorites"


class TestFavoritesJobDetailView(
    TestCase,
    GetResponseMixin,
    RedirectIfNoUserMixin,
    RedirectIfWrongUserMixin,
    SingleObjectContextMixin,
):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username="TestUser1", email="testuser1@testemail.com"
        )
        user2 = User.objects.create(
            username="TestUser2", email="testuser2@testemail.com"
        )
        user1.set_password("testpassword")
        user2.set_password("testpassword")
        user1.save()
        user2.save()
        FavoriteJobQuery.objects.create(title="TestTitle", account=user1)
        FavoriteJobQuery.objects.create(title="TestTitle", account=user2)

    def setUp(self):
        self.url = "/favorites/jobs/1"
        self.template_name = "scrpr/content_with_sidebar/favorites_job.html"
        self.template_base = (
            "scrpr/content_with_sidebar/content_with_sidebar_base.html"
        )
        self.model = FavoriteJobQuery
        self.client.login(username="TestUser1", password="testpassword")
        self.next = "/favorites/jobs/1"
        self.success_url = "/favorites"


class TestFavoritesGameDeleteView(
    TestCase,
    GetResponseMixin,
    RedirectIfNoUserMixin,
    RedirectIfWrongUserMixin,
    ObjectDeletionWithRedirectMixin,
):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username="TestUser1", email="testuser1@testemail.com"
        )
        user2 = User.objects.create(
            username="TestUser2", email="testuser2@testemail.com"
        )
        user1.set_password("testpassword")
        user2.set_password("testpassword")
        user1.save()
        user2.save()
        FavoriteGameQuery.objects.create(
            title="TestName", free=True, account=user1
        )

    def setUp(self):
        self.url = "/favorites/games/1/delete"
        self.template_name = (
            "scrpr/content_with_sidebar/delete_favorites_game.html"
        )
        self.template_base = (
            "scrpr/content_with_sidebar/content_with_sidebar_base.html"
        )
        self.model = FavoriteGameQuery
        self.redirect_url = "/favorites"
        self.client.login(username="TestUser1", password="testpassword")
        self.next = "/favorites/games/1/delete"
        self.success_url = "/favorites"


class TestFavoritesJobDeleteView(
    TestCase,
    GetResponseMixin,
    RedirectIfNoUserMixin,
    RedirectIfWrongUserMixin,
    ObjectDeletionWithRedirectMixin,
):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username="TestUser1", email="testuser1@testemail.com"
        )
        user2 = User.objects.create(
            username="TestUser2", email="testuser2@testemail.com"
        )
        user1.set_password("testpassword")
        user2.set_password("testpassword")
        user1.save()
        user2.save()
        FavoriteJobQuery.objects.create(title="TestTitle", account=user1)

    def setUp(self):
        self.url = "/favorites/jobs/1/delete"
        self.template_name = (
            "scrpr/content_with_sidebar/delete_favorites_job.html"
        )
        self.template_base = (
            "scrpr/content_with_sidebar/content_with_sidebar_base.html"
        )
        self.model = FavoriteGameQuery
        self.redirect_url = "/favorites"
        self.client.login(username="TestUser1", password="testpassword")
        self.next = "/favorites/jobs/1/delete"
        self.success_url = "/favorites"


class TestAboutView(TestCase, GetResponseMixin):
    def setUp(self):
        self.url = "/about"
        self.template_name = "scrpr/about.html"


class TestRateView(TestCase, GetResponseMixin, FormValidationMixin):
    def setUp(self):
        self.url = "/rate"
        self.template_name = "scrpr/rate.html"
        self.success_url = "/"
        self.model = Comment
        self.invalid_form_samples = (RATE_INVALID_FORM,)
        self.invalid_form_errors = (RATE_ERRORS,)
        self.valid_form_sample = RATE_VALID_FORM

    def test_valid_form_submission(self):
        response = self.client.post(self.url, RATE_VALID_FORM)
        self.assertEqual(response.status_code, 302)
        object = self.model.objects.get(pk=1)
        self.assertTrue(object.name, RATE_VALID_FORM["name"])
        self.assertTrue(object.comment, RATE_VALID_FORM["comment"])


class TestGamesView(TestCase, GetResponseMixin, WebScrapingResultsMixin):
    def setUp(self):
        self.url = "/games"
        self.template_name = "scrpr/content_with_sidebar/games.html"
        self.template_base = (
            "scrpr/content_with_sidebar/content_with_sidebar_base.html"
        )
        self.queries = [
            "?title=deus+ex",
            "?initial_price=on",
            "?psplus_price=on",
            "?title=deus+ex&initial_price=on&psplus_price=on",
            "?title=deus+ex&psplus_price=on",
            "?initial_price=on&psplus_price=on",
            "?title=deus+ex&price_min=100&price_max=10000",
            "?free=on",
            "?title=deus+ex&free=on",
        ]


class TestJobsView(TestCase, GetResponseMixin, WebScrapingResultsMixin):
    def setUp(self):
        self.url = "/jobs"
        self.template_name = "scrpr/content_with_sidebar/jobs.html"
        self.template_base = (
            "scrpr/content_with_sidebar/content_with_sidebar_base.html"
        )
        self.queries = [
            "?title=Python",
            "?city=Одесса",
            "?title=Python?city=Киев",
            "?title=Python&salary_min=1000&salary_max=100000",
            "?title=Python&salary_min=1000&salary_max=100000&with_salary=on",
            "?salary_min=1000&salary_max=100000",
            "?title=Python&city=Одесса&with_salary=on",
        ]


class TestLogoutView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username="TestUser1", email="testuser1@testemail.com"
        )
        user1.set_password("testpassword")
        user1.save()

    def setUp(self):
        self.url = "/logout"
        self.protected_url = "/favorites"
        self.client.login(username="TestUser1", password="testpassword")
        self.next = "/"

    def test_logout_redirect(self):
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.next)
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 302)
