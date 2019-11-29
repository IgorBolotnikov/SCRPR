from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from authentication.models import User
from .models import SavedSuggestion
from scrpr.models import Game, Job


# workflow of cron job:
# For every User:
# 1. If User has notifications set up, and frequency is the same:
#     1. Form a query from notification parameters (limited by 10 results)
#     2. Check previous suggestions in SavedSuggestion model
#     3. If there are any of them of the same type:
#         1. Remode the doubling suggestions from the query
#            for every repeating suggestion already saved in database
#        Else:
#         1. Do nothing with query results, continue to the next step
#     4. If by this point any query results remaining:
#         1. Form a message to User email with query results
#            in respective template (template is chosen by suggestion type)
#         2. Send message to User
#         3. If there are already 5 suggestion packs from messages
#            saved in database:
#             1. Remove the oldest pack and save current query in the database
#            Else:
#             1. Just save the query in the database
#        Else:
#         1. Do nothing and switch to the next User


class Suggestion:
    def __init__(self, frequency_in_days):
        self.frequency_in_days = frequency_in_days

    def _get_users_with_favorites(self):
        return User.objects.filter(
            Q(favoritegamequery__notification_freq=self.frequency_in_days) | Q(
              favoritejobquery__notification_freq=self.frequency_in_days))

    @staticmethod
    def _get_job_favorites(user):
        return user.favoritejobquery_set.all()

    @staticmethod
    def _get_game_favorites(user):
        return user.favoritegamequery_set.all()

    @staticmethod
    def _get_saved_suggestions(user, type):
        return SavedSuggestion.objects.filter(account=user, type=type)

    def _get_filtered_suggestions(self, new_suggestions, user, type):
        prev_suggestions = self._get_saved_suggestions(user, type)
        return self._remove_dublicates(
            new_suggestions, prev_suggestions.only('link'))

    @staticmethod
    def _remove_dublicates(new_list, old_list):
        result = []
        for entry in new_list:
            if entry.link not in old_list:
                result.append(entry)
        return result

    @staticmethod
    def _get_email_context(suggestions, username, frequency):
        return {
            'object_list': suggestions,
            'username': username,
            'frequency': frequency,
        }

    @staticmethod
    def save_new_suggestions(new_suggestions, type, user):
        new_entries = [
            SavedSuggestion(type=type, link=suggestion.link, account=user) for suggestion in new_suggestions
        ]
        SavedSuggestion.objects.bulk_create(new_entries)

    @staticmethod
    def _send_message(subject_filename, body_txt_filename,
                     body_html_filename, receiver_email, email_context):
        subject_template = get_template('smart_emails/' + subject_filename)
        text_email_template = get_template('smart_emails/' + body_txt_filename)
        html_email_template = get_template('smart_emails/' + body_html_filename)
        rendered_subject = subject_template.render().strip()
        txt_with_context = text_email_template.render(email_context)
        html_with_context = html_email_template.render(email_context)
        message = EmailMultiAlternatives(
            rendered_subject,
            txt_with_context,
            settings.EMAIL_HOST_USER,
            [receiver_email]
        )
        message.attach_alternative(html_with_context, 'text/html')
        message.send()

    def _get_game_suggestions_from_query(self, query_items):
        if not query_items:
            return Game.objects.all()[:10]
        queryset = Game.objects
        for key, value in query_items.items():
            if key == 'title' and value:
                queryset = queryset.filter(title__icontains=value)
            elif key == 'price_min' and value:
                queryset = queryset.filter(
                    Q(price__gte=value) | Q(psplus_price__gte=value))
            elif key == 'price_max' and value:
                queryset = queryset.filter(
                    Q(price__lte=value) | Q(psplus_price__lte=value))
            elif key == 'psplus_price' and value:
                queryset = queryset.filter(psplus_price__isnull=False)
            elif key == 'initial_price' and value:
                queryset = queryset.filter(initial_price__isnull=False)
            elif key == 'free' and value:
                queryset = queryset.filter(Q(price=0.00) | Q(psplus_price=0.00))
        return queryset.all()[:10]

    def _get_job_suggestions_from_query(self, query_items):
        if not query_items:
            return Job.objects.all()[:10]
        queryset = Job.objects
        for key, value in query_items.items():
            if key == 'title' and value:
                queryset = queryset.filter(title__icontains=value)
            elif key == 'city' and value:
                queryset = queryset.filter(location=value)
            elif key == 'salary_min' and value:
                queryset = queryset.filter(salary_min__gte=value)
            elif key == 'salary_max' and value:
                queryset = queryset.filter(salary_max__lte=value)
            elif key == 'with_salary' and value:
                queryset = queryset.filter(
                    salary_min__isnull=False, salary_max__isnull=False)
        return queryset.all()[:10]

    def _send_game_suggestions(self, game_favorites, user):
        for game_favorite in game_favorites.values():
            game_suggestions = self._get_game_suggestions_from_query(game_favorite)
            if game_suggestions:
                filtered_suggestions = self._get_filtered_suggestions(
                    game_suggestions, user, 'JOB')
                if filtered_suggestions:
                    email_context = self._get_email_context(
                        filtered_suggestions,
                        user.username,
                        self.frequency
                    )
                    self._send_message(
                        subject_filename='games_email_subject_template.txt',
                        body_txt_filename='games_email_body_template.txt',
                        body_html_filename='games_email_body_template.html',
                        receiver_email=user.email,
                        email_context=email_context
                    )
                    self.save_new_suggestions(filtered_suggestions, 'GAME', user)

    def _send_job_suggestions(self, job_favorites, user):
        for job_favorite in job_favorites.values():
            job_suggestions = self._get_job_suggestions_from_query(job_favorite)
            if job_suggestions:
                filtered_suggestions = self._get_filtered_suggestions(
                    job_suggestions, user, 'JOB')
                if filtered_suggestions:
                    email_context = self._get_email_context(
                        filtered_suggestions,
                        user.username,
                        self.frequency
                    )
                    self._send_message(
                        subject_filename='jobs_email_subject_template.txt',
                        body_txt_filename='jobs_email_body_template.txt',
                        body_html_filename='jobs_email_body_template.html',
                        receiver_email=user.email,
                        email_context=email_context
                    )
                    self.save_new_suggestions(filtered_suggestions, 'JOB', user)

    def send_suggestions(self):
        users = self._get_users_with_favorites()
        for user in users:
            game_favorites = self._get_game_favorites(user)
            if game_favorites:
                self._send_game_suggestions(game_favorites, user)
            job_favorites = self._get_job_favorites(user)
            if job_favorites:
                self._send_job_suggestions(job_favorites, user)

    @property
    def frequency(self):
        from scrpr.constants import CHOICES_DICT
        return CHOICES_DICT[self.frequency_in_days]
