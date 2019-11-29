from .updatescrapeddata import *


class Command(CommandBase):
    def handle(self, *args, **options):
        self.load_jobs_data()
        self.load_games_data()
        self.stdout.write(self.style.SUCCESS(SUCCESS_MESSAGE))
