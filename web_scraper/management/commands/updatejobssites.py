from .updatescrapeddata import *


class Command(CommandBase):
    def handle(self, *args, **options):
        scrape_jobs.JobisScraper().scrape_job_website()
        scrape_jobs.JobsScraper().scrape_job_website()
        scrape_jobs.JoobleScraper().scrape_job_website()
        scrape_jobs.NovarobotaScraper().scrape_job_website()
        scrape_jobs.TrudScraper().scrape_job_website()
