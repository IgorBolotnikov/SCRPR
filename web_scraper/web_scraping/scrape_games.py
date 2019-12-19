from .scrape_base import *


class PSStoreScraper(ScraperBase):
    def _get_url(self, page_num=1, query_params=None):
        '''
        Get url for parsing with specified query params
        '''
        DEFAULT_MIN_PRICE = 0
        DEFAULT_MAX_PRICE = 1000000
        title = query_params.get('title') if query_params.get('title') else ''
        price_min = int(query_params.get('price_min')) * 100 \
                    if query_params.get('price_min') else DEFAULT_MIN_PRICE
        price_max = int(query_params.get('price_max')) * 100 \
                    if query_params.get('price_max') else DEFAULT_MAX_PRICE
        psplus_price = bool(query_params.get('psplus_price'))
        initial_price = bool(query_params.get('initial_price'))
        free = bool(query_params.get('free'))
        price_min, price_max = (0, 0) if query_params.get('free') else (price_min, price_max)
        # page_num = query_params.get('page') if query_params.get('page') else page_num
        self.params = {
            'gameContentType': 'games,bundles',
            'query': title,
            'price': f'{price_min}-{price_max}',
        }
        if title:
            return f'{PS_STORE_INIT_LINK}{page_num}'
        elif initial_price:
            return f'{PS_STORE_DISCOUNT_LINK}{page_num}'
        elif psplus_price or free:
            # In this case page nums are simply used to iterate through each link
            # In a list of different PS Plus offers, because these pages
            # Never get more than 1 page each
            return PS_STORE_PSPLUS_GAMES[page_num - 1]
        return f'{PS_STORE_INIT_LINK}{page_num}'

    @staticmethod
    def _get_last_page_num(page):
        last = page.find_all('a', class_='paginator-control__end')
        if last: last = last[0].get('href')
        if last: last = last.split('/')[-1].split('?')[0]
        return int(last) if last else 1

    @staticmethod
    def _get_games_list(page):
        PRICE_CLASSES = (
            'price-display__price',
            'price-display__price--is-plus-exclusive'
        )
        game_divs = []
        game_divs.extend(page.find_all('div', class_='grid-cell--game'))
        game_divs.extend(page.find_all('div', class_='grid-cell--game-related'))
        games = []
        for game_div in game_divs:
            if game_div.find('h3', class_=PRICE_CLASSES[0]) \
            or game_div.find('h3', class_=PRICE_CLASSES[1]):
                games.append(game_div)
        return games

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
        price = game.find('h3', class_='price-display__price')
        price = price.get_text() if price else '0'

        psplus_price1 = game.find(
            'div', class_='price-display__price--is-plus-upsell')
        psplus_price1 = psplus_price1.get_text() if psplus_price1 else None

        psplus_price2 = game.find(
            'h3', class_='price-display__price--is-plus-exclusive')
        psplus_price2 = psplus_price2.get_text() if psplus_price2 else None

        psplus_price = psplus_price2 if psplus_price2 else psplus_price1

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
