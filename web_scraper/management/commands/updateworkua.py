from .updatescrapeddata import *


class Command(CommandBase):
    def handle(self, *args, **options):
        scrape_jobs.WorkScraper().scrape_job_website()
