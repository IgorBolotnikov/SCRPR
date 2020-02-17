import pytest
from web_scraper.web_scraping import scrape_games, scrape_jobs


class TestJobScraping:
    def test_results(self):
        results = scrape_jobs.JobsSitesScraper().scrape_websites(None, 1, {})
        assert results.get('last_page'), 'Should return last page value'
        assert results.get('object_list'), 'Should return results'
        assert len(results['object_list']) > 0, 'Should be more than 0 results'


class TestGamesScraping:
    def test_results(self):
        results = scrape_games.PSStoreScraper().scrape_game_website(1, {})
        assert results.get('last_page'), 'Should return last page value'
        assert results.get('object_list'), 'Should return results'
        assert len(results['object_list']) > 0, 'Should be more than 0 results'
        results = scrape_games.PSStoreScraper().scrape_game_website(1, {
            'initial_price': True,
            'title': 'Deus Ex'
        })
        assert 'last_page' in results.keys(), 'Should return last page value'
        assert 'object_list' in results.keys(), 'Should return results'
