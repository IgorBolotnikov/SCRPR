from .updatescrapeddata import *
SUCCESS_MESSAGE = 'Scraped data was successfully cleared'


class Command(CommandBase):
    def handle(self, *args, **options):
        Jobs.objects.all().delete()
        Game.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(SUCCESS_MESSAGE))
