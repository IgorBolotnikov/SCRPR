from datetime import datetime, timezone
from django.core import mail
from django.test import TestCase, SimpleTestCase, Client

from .views import *
from .models import *
from authentication.models import User


LOGIN_URL = '/auth/login/?next='

# ===== Always present templates =====

BASE_TEMPLATE = 'scrpr/base.html'
NAVBAR_TEMPLATE = 'scrpr/navbar.html'
FOOTER_TEMPLATE = 'scrpr/footer.html'

NAVBAR_USER_LINKS = ('Log Out', 'My Account')
NAVBAR_NOUSER_LINKS = ('Log In', 'Register')


# ===== Forms (valid, invalid, errors) =====

# Valid forms
RATE_VALID_FORM = {
    'name': 'TestName',
    'comment': 'Test Comment'
}

# Invalid forms and form errors
RATE_INVALID_FORM = {
    'name': ''.join(['q' for q in range(101)]),
    'comment': 'Anyway valid comment'
}
RATE_ERRORS = {
    'name': 'Ensure this value has at most 100 characters (it has 101).',
    'comment': None
}


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


class TestSingleObjectContextMixin:
    def test_object_context(self):
        test_object = self.model.objects.get(pk=1)
        response = self.client.get(self.url)
        self.assertEqual(response.context['object'].id, 1)
        self.assertEqual(response.context['object'], test_object)


class TestRedirectIfNoUserMixin:
    def test_redirect_if_no_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, LOGIN_URL + self.next)


class TestRedirectIfWrongUserMixin:
    def test_redirect_if_wrong_user(self):
        self.client.login(
            username='TestUser2',
            password='testpassword'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

#
class TestWebScrapingResultsMixin:
    def test_scraping_results_with_var_queries(self):
        response = self.client.get(self.url)
        self.assertTrue(
            len(response.context['object_list']) > 0,
            f'Web search from URL "{self.url} did not return any results"'
        )
        for query in self.queries:
            query_url = self.url + query
            response = self.client.get(query_url)
            self.assertTrue(
                response.context['object_list'] is not None,
                f'Web search from URL "{query_url} did not return results list"'
            )


class TestMainPageView(TestCase, TestGetResponseMixin):
    def setUp(self):
        self.url = ''
        self.template_name = 'scrpr/index.html'

class TestNewsListView(TestCase,
                       TestGetResponseMixin,
                       TestModelInstancesContextMixin):
    @classmethod
    def setUpTestData(cls):
        news1 = NewsPost.objects.create(
            title='Test1',
            body='<p>Test Body1</p>',
            datetime_posted=datetime.now(timezone.utc)
        )
        news2 = NewsPost.objects.create(
            title='Test2',
            body='<p>Test Body2</p>',
            datetime_posted=datetime.now(timezone.utc)
        )

    def setUp(self):
        self.url = '/news'
        self.template_name = 'scrpr/news.html'
        self.model = NewsPost


class TestFavoritesView(TestCase,
                        TestGetResponseMixin,
                        TestRedirectIfNoUserMixin):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='TestUser1',
            email='testuser1@testemail.com'
        )
        user.set_password('testpassword')
        user.save()
        game_fav1 = FavoriteGameQuery.objects.create(
            title='TestName',
            free=True,
            account=user
        )
        job_fav1 = FavoriteJobQuery.objects.create(
            title='Test title',
            account=user
        )

    def setUp(self):
        self.url = '/favorites'
        self.template_name = 'scrpr/content_with_sidebar/favorites.html'
        self.template_base = 'scrpr/content_with_sidebar/content_with_sidebar_base.html'
        self.client.login(
            username='TestUser1',
            password='testpassword'
        )
        self.games_model = FavoriteGameQuery
        self.jobs_model = FavoriteJobQuery
        self.next = '/favorites'

    def test_games_favorites_context(self):
        test_objects = [repr(object) for object in self.games_model.objects.all()]
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['object_list_games'],
            test_objects,
            ordered=False
        )

    def test_jobs_favorites_context(self):
        test_objects = [repr(object) for object in self.jobs_model.objects.all()]
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['object_list_jobs'],
            test_objects,
            ordered=False
        )


class TestFavoritesGameDetailView(TestCase,
                                  TestGetResponseMixin,
                                  TestRedirectIfNoUserMixin,
                                  TestRedirectIfWrongUserMixin,
                                  TestSingleObjectContextMixin):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='TestUser1',
            email='testuser1@testemail.com'
        )
        user2 = User.objects.create(
            username='TestUser2',
            email='testuser2@testemail.com'
        )
        user1.set_password('testpassword')
        user2.set_password('testpassword')
        user1.save()
        user2.save()
        game_fav1 = FavoriteGameQuery.objects.create(
            title='TestName',
            free=True,
            account=user1
        )
        game_fav2 = FavoriteGameQuery.objects.create(
            title='TestName',
            free=True,
            account=user2
        )
        job_fav1 = FavoriteJobQuery.objects.create(
            title='Test title',
            account=user1
        )

    def setUp(self):
        self.url = '/favorites/games/1'
        self.template_name = 'scrpr/content_with_sidebar/favorites_game.html'
        self.template_base = 'scrpr/content_with_sidebar/content_with_sidebar_base.html'
        self.model = FavoriteGameQuery
        self.client.login(
            username='TestUser1',
            password='testpassword'
        )
        self.next = '/favorites/games/1'
        self.success_url = '/favorites'


class TestFavoritesJobDetailView(TestCase,
                                 TestGetResponseMixin,
                                 TestRedirectIfNoUserMixin,
                                 TestRedirectIfWrongUserMixin,
                                 TestSingleObjectContextMixin):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='TestUser1',
            email='testuser1@testemail.com'
        )
        user2 = User.objects.create(
            username='TestUser2',
            email='testuser2@testemail.com'
        )
        user1.set_password('testpassword')
        user2.set_password('testpassword')
        user1.save()
        user2.save()
        job_fav1 = FavoriteJobQuery.objects.create(
            title='TestTitle',
            account=user1
        )
        job_fav2 = FavoriteJobQuery.objects.create(
            title='TestTitle',
            account=user2
        )

    def setUp(self):
        self.url = '/favorites/jobs/1'
        self.template_name = 'scrpr/content_with_sidebar/favorites_job.html'
        self.template_base = 'scrpr/content_with_sidebar/content_with_sidebar_base.html'
        self.model = FavoriteJobQuery
        self.client.login(
            username='TestUser1',
            password='testpassword'
        )
        self.next = '/favorites/jobs/1'
        self.success_url = '/favorites'


class TestFavoritesGameDeleteView(TestCase,
                                  TestGetResponseMixin,
                                  TestRedirectIfNoUserMixin,
                                  TestRedirectIfWrongUserMixin,
                                  TestObjectDeletionWithRedirectMixin):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='TestUser1',
            email='testuser1@testemail.com'
        )
        user2 = User.objects.create(
            username='TestUser2',
            email='testuser2@testemail.com'
        )
        user1.set_password('testpassword')
        user2.set_password('testpassword')
        user1.save()
        user2.save()
        game_fav1 = FavoriteGameQuery.objects.create(
            title='TestName',
            free=True,
            account=user1
        )

    def setUp(self):
        self.url = '/favorites/games/1/delete'
        self.template_name = 'scrpr/content_with_sidebar/delete_favorites_game.html'
        self.template_base = 'scrpr/content_with_sidebar/content_with_sidebar_base.html'
        self.model = FavoriteGameQuery
        self.redirect_url = '/favorites'
        self.client.login(
            username='TestUser1',
            password='testpassword'
        )
        self.next='/favorites/games/1/delete'
        self.success_url = '/favorites'


class TestFavoritesJobDeleteView(TestCase,
                                 TestGetResponseMixin,
                                 TestRedirectIfNoUserMixin,
                                 TestRedirectIfWrongUserMixin,
                                 TestObjectDeletionWithRedirectMixin):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='TestUser1',
            email='testuser1@testemail.com'
        )
        user2 = User.objects.create(
            username='TestUser2',
            email='testuser2@testemail.com'
        )
        user1.set_password('testpassword')
        user2.set_password('testpassword')
        user1.save()
        user2.save()
        job_fav1 = FavoriteJobQuery.objects.create(
            title='TestTitle',
            account=user1
        )

    def setUp(self):
        self.url = '/favorites/jobs/1/delete'
        self.template_name = 'scrpr/content_with_sidebar/delete_favorites_job.html'
        self.template_base = 'scrpr/content_with_sidebar/content_with_sidebar_base.html'
        self.model = FavoriteGameQuery
        self.redirect_url = '/favorites'
        self.client.login(
            username='TestUser1',
            password='testpassword'
        )
        self.next='/favorites/jobs/1/delete'
        self.success_url = '/favorites'


class TestAboutView(TestCase, TestGetResponseMixin):
    def setUp(self):
        self.url = '/about'
        self.template_name = 'scrpr/about.html'


class TestRateView(TestCase,
                   TestGetResponseMixin,
                   TestFormValidationMixin):
    def setUp(self):
        self.url = '/rate'
        self.template_name = 'scrpr/rate.html'
        self.success_url = '/'
        self.model = Comment
        self.invalid_form_samples = (RATE_INVALID_FORM,)
        self.invalid_form_errors = (RATE_ERRORS,)
        self.valid_form_sample = RATE_VALID_FORM

    def test_valid_form_submission(self):
        response = self.client.post(self.url, RATE_VALID_FORM)
        self.assertEqual(response.status_code, 302)
        object = self.model.objects.get(pk=1)
        self.assertTrue(object.name, RATE_VALID_FORM['name'])
        self.assertTrue(object.comment, RATE_VALID_FORM['comment'])


class TestGamesView(TestCase, TestGetResponseMixin, TestWebScrapingResultsMixin):
    def setUp(self):
        self.url = '/games/'
        self.template_name = 'scrpr/content_with_sidebar/games.html'
        self.template_base = 'scrpr/content_with_sidebar/content_with_sidebar_base.html'
        self.queries = [
            '?title=deus+ex',
            '?initial_price=on',
            '?psplus_price=on',
            '?title=deus+ex&initial_price=on&psplus_price=on',
            '?title=deus+ex&psplus_price=on',
            '?initial_price=on&psplus_price=on',
            '?title=deus+ex&price_min=100&price_max=10000'
        ]


class TestJobsView(TestCase, TestGetResponseMixin, TestWebScrapingResultsMixin):
    def setUp(self):
        self.url = '/jobs/'
        self.template_name = 'scrpr/content_with_sidebar/jobs.html'
        self.template_base = 'scrpr/content_with_sidebar/content_with_sidebar_base.html'
        self.queries = [
            '?title=Python',
            '?city=Одесса',
            '?title=Python?city=Киев',
            '?title=Python&salary_min=1000&salary_max=100000',
            '?title=Python&salary_min=1000&salary_max=100000&with_salary=on',
            '?salary_min=1000&salary_max=100000',
            '?title=Python&city=Одесса&with_salary=on'
        ]


class TestLogoutView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='TestUser1',
            email='testuser1@testemail.com'
        )
        user1.set_password('testpassword')
        user1.save()

    def setUp(self):
        self.url = '/logout'
        self.protected_url = '/favorites'
        self.client.login(
            username='TestUser1',
            password='testpassword'
        )
        self.next = '/'

    def test_logout_redirect(self):
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.next)
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 302)
