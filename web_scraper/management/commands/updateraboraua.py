from .updatescrapeddata import *


class Command(CommandBase):
    def handle(self, *args, **options):
        scrape_jobs.RabotaScraper().scrape_job_website()
