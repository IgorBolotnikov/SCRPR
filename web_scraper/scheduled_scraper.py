from web_scraping import scrape_jobs, scrape_games
from scrpr.models import Job, Game
from itertools import islice


def update_jobs_db():
    file_list = [
        RABOTAUA_FILE,
        WORKUA_FILE,
        JOBSUA_FILE,
        JOOBLEORG_FILE,
        JOBISCOMUA_FILE,
        NOVAROBOTAUA_FILE,
        TRUDUA_FILE,
    ]
    Job().objects.all().delete()
    for filename in file_list:
        with open(filename) as json_file:
            json_data = json.load(json_file)
            batch_size = 100
            jobs = [
                Job(title=line['title'],
                    body=line['body'],
                    location=line['location'],
                    salary_min=line['salary_min'],
                    salary_max=line['salary_max'],
                    currency=line['currency'],
                    employer=line['employer'],
                    line=line['link'],
                    source=line['source']
                ) for line in json_data
            ]
            while True:
                batch = list(islice(jobs, batch_size))
                if not batch:
                    break
                Job.objects.bulk_create(batch, batch_size)



if __name__ == '__main__':
    update_jobs_db()
    # scrape_jobs.JobisScraper().scrape_job_website()
    # scrape_jobs.JobsScraper().scrape_job_website()
    # scrape_jobs.JoobleScraper().scrape_job_website()
    # scrape_jobs.NovarobotaScraper().scrape_job_website()
    # scrape_jobs.RabotaScraper().scrape_job_website()
    # scrape_jobs.TrudScraper().scrape_job_website()
    # scrape_jobs.WorkScraper().scrape_job_website()
    # scrape_games.PSStoreScraper().scrape_game_website()
