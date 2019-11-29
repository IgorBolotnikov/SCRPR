from .updatescrapeddata import *


class Command(CommandBase):
    def handle(self, *args, **options):
        scrape_games.PSStoreScraper().scrape_game_website()
