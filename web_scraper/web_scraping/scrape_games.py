from .scrape_base import *


class PSStoreScraper(ScraperBase):

    def __init__(self):
        self.filename = PS_STORE_FILE

    @staticmethod
    def _get_url(): return PS_STORE_LINK

    @staticmethod
    def _get_last_page_num(page):
        last = page.find_all('a', class_='paginator-control__end')[0].get('href')
        return int(last.split('/')[-1]) if last else None

    @staticmethod
    def _get_games_list(page):
        games = page.find_all('div', class_='grid-cell--game')
        return [game for game in games if game.find('h3', class_='price-display__price')]

    @staticmethod
    def _get_game_title(game):
        title = game.find('div', class_='grid-cell__title').find('span').get_text()
        parsed_title = ''
        for char in title:
            if char != '\\':
                parsed_title += char
        title = parsed_title
        return title

    @staticmethod
    def  _get_game_price(game):
        price = game.find('h3', class_='price-display__price').get_text()
        psplus_price = game.find(
            'div', class_='price-display__price--is-plus-upsell')
        psplus_price = psplus_price.get_text() if psplus_price else None
        initial_price = game.find('span', class_="price-display__strikethrough")
        initial_price = initial_price.div.get_text() if initial_price else None
        return price, psplus_price, initial_price

    @staticmethod
    def _get_game_image(game):
        images = game.find('div', class_='product-image__img--main').img['srcset']
        return images.split(' 2x,')[0].split(' 1.5x, ')[1]

    @staticmethod
    def _get_game_link(game):
        game_link = game.find('a', class_='internal-app-link').get('href')
        return PS_STORE_BASELINK + game_link
