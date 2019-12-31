from django.core.management.base import BaseCommand
from scrpr.models import Job, Game
from itertools import islice
from web_scraper.web_scraping import scrape_jobs, scrape_games
import json


JOB_FILE_LIST = [
    scrape_jobs.RABOTAUA_FILE,
    scrape_jobs.WORKUA_FILE,
    scrape_jobs.JOBSUA_FILE,
    scrape_jobs.JOOBLEORG_FILE,
    scrape_jobs.JOBISCOMUA_FILE,
    scrape_jobs.NOVAROBOTAUA_FILE,
    scrape_jobs.TRUDUA_FILE,
]
GAME_FILE_LIST = [
    scrape_games.PS_STORE_FILE,
]
BATCH_SIZE = 100
SUCCESS_MESSAGE = 'Scraped data have been successfully loaded to db'


class CommandBase(BaseCommand):

    @staticmethod
    def scrape_websites():
        scrape_jobs.JobisScraper().scrape_job_website()
        scrape_jobs.JobsScraper().scrape_job_website()
        scrape_jobs.JoobleScraper().scrape_job_website()
        scrape_jobs.NovarobotaScraper().scrape_job_website()
        scrape_jobs.RabotaScraper().scrape_job_website()
        scrape_jobs.TrudScraper().scrape_job_website()
        scrape_jobs.WorkScraper().scrape_job_website()
        scrape_games.PSStoreScraper().scrape_game_website()

    @staticmethod
    def _load_json_file(filename):
        with open(filename) as json_file:
            return json.load(json_file)

    @staticmethod
    def _create_job_entries(json_data):
        jobs = (
            Job(title=line['title'],
                body=line['body'],
                location=line['location'],
                salary_min=line['salary_min'],
                salary_max=line['salary_max'],
                currency=line['currency'],
                employer=line['employer'],
                link=line['link'],
                source=line['source']
            ) for line in json_data
        )
        # artificial limitation because of
        # limited database storage on heroku
        for counter in range(8):
            batch = list(islice(jobs, BATCH_SIZE))
            if not batch:
                break
            Job.objects.bulk_create(batch, BATCH_SIZE)

    @staticmethod
    def _create_game_entries(json_data):
        games = (
            Game(title=line['title'],
                 price=line['price'],
                 psplus_price=line['psplus_price'],
                 initial_price=line['initial_price'],
                 image=line['image'],
                 link=line['link']
            ) for line in json_data
        )
        # artificial limitation because of
        # limited database storage on heroku
        for counter in range(10):
            batch = list(islice(games, BATCH_SIZE))
            if not batch:
                break
            Game.objects.bulk_create(batch, BATCH_SIZE)

    def load_jobs_data(self):
        Job.objects.all().delete()
        for filename in JOB_FILE_LIST:
            self._create_job_entries(self._load_json_file(filename))

    def load_games_data(self):
        Game.objects.all().delete()
        for filename in GAME_FILE_LIST:
            self._create_game_entries(self._load_json_file(filename))


class Command(CommandBase):
    help = 'update db with scraped data (jobs and games)'

    def handle(self, *args, **options):
        self.scrape_websites()
        self.load_jobs_data()
        self.load_games_data()
        self.stdout.write(self.style.SUCCESS(SUCCESS_MESSAGE))
