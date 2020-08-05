from unittest.mock import patch

import pytest
from mixer.backend.django import mixer

from .. import cron_daily, cron_monthly, cron_weekly
from ..models import SavedSuggestion

pytestmark = pytest.mark.django_db


class TestDailyCron:
    @patch("smart_emails.suggestions.sendgrid")
    def test_successfull_cron(self, mock_sendgrid):
        game_patcher = patch("smart_emails.suggestions.PSStoreScraper")
        game_mock = game_patcher.start()
        game_mock = game_mock()
        game_mock.scrape_game_website.return_value = {
            "object_list": [{"link": "result1"}, {"link": "result2"}],
            "last_page": 1,
        }
        job_patcher = patch("smart_emails.suggestions.JobsSitesScraper")
        job_mock = job_patcher.start()
        job_mock = job_mock()
        job_mock.scrape_websites.return_value = {
            "object_list": [{"link": "result1"}, {"link": "result2"}],
            "last_page": 1,
        }
        mixer.blend("scrpr.FavoriteGameQuery", notification_freq=1)
        mixer.blend("scrpr.FavoriteJobQuery", notification_freq=7)
        cron_daily.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 2, "Should send only daily suggestions"

    @patch("smart_emails.suggestions.sendgrid")
    def test_unsucessfull_cron(self, mock_sendgrid):
        cron_daily.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 0, "Should not be any saved suggestions"


class TestWeeklyCron:
    @patch("smart_emails.suggestions.sendgrid")
    def test_successfull_cron(self, mock_sendgrid):
        date_patcher = patch("smart_emails.cron_weekly.datetime")
        date_mock = date_patcher.start().today()
        date_mock.weekday.return_value = 0

        game_patcher = patch("smart_emails.suggestions.PSStoreScraper")
        game_mock = game_patcher.start()
        game_mock = game_mock()
        game_mock.scrape_game_website.return_value = {
            "object_list": [{"link": "result1"}, {"link": "result2"}],
            "last_page": 1,
        }
        job_patcher = patch("smart_emails.suggestions.JobsSitesScraper")
        job_mock = job_patcher.start()
        job_mock = job_mock()
        job_mock.scrape_websites.return_value = {
            "object_list": [{"link": "result1"}, {"link": "result2"}],
            "last_page": 1,
        }
        mixer.blend("scrpr.FavoriteGameQuery", notification_freq=7)
        mixer.blend("scrpr.FavoriteJobQuery", notification_freq=1)
        cron_weekly.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 2, "Should send only weekly suggestions"

    @patch("smart_emails.suggestions.sendgrid")
    def test_unsucessfull_cron(self, mock_sendgrid):
        date_patcher = patch("smart_emails.cron_weekly.datetime")
        date_mock = date_patcher.start().today()
        date_mock.weekday.return_value = 1
        cron_weekly.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 0, "Should not be any saved suggestions"
        date_mock.weekday.return_value = 0
        cron_weekly.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 0, "Should not be any saved suggestions"


class TestMonthlyCron:
    @patch("smart_emails.suggestions.sendgrid")
    def test_successfull_cron(self, mock_sendgrid):
        date_patcher = patch("smart_emails.cron_monthly.datetime")
        date_mock = date_patcher.start().today()
        date_mock.day = 1

        game_patcher = patch("smart_emails.suggestions.PSStoreScraper")
        game_mock = game_patcher.start()
        game_mock = game_mock()
        game_mock.scrape_game_website.return_value = {
            "object_list": [{"link": "result1"}, {"link": "result2"}],
            "last_page": 1,
        }
        job_patcher = patch("smart_emails.suggestions.JobsSitesScraper")
        job_mock = job_patcher.start()
        job_mock = job_mock()
        job_mock.scrape_websites.return_value = {
            "object_list": [{"link": "result1"}, {"link": "result2"}],
            "last_page": 1,
        }
        mixer.blend("scrpr.FavoriteGameQuery", notification_freq=7)
        mixer.blend("scrpr.FavoriteJobQuery", notification_freq=30)
        cron_monthly.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 2, "Should send only monthly suggestions"

    @patch("smart_emails.suggestions.sendgrid")
    def test_unsucessfull_cron(self, mock_sendgrid):
        date_patcher = patch("smart_emails.cron_monthly.datetime")
        date_mock = date_patcher.start().today()
        date_mock.day = 2
        cron_monthly.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 0, "Should not be any saved suggestions"
        date_mock.day = 1
        cron_monthly.send_suggestions()
        suggestions = SavedSuggestion.objects.all()
        assert len(suggestions) == 0, "Should not be any saved suggestions"
