import os
import json
import lxml
import asyncio
import aiohttp
import requests
from random import random
from urllib.request import urlopen, Request
from urllib.parse import quote, urlencode
from time import time, sleep
from datetime import datetime
from bs4 import BeautifulSoup as soup
from .constants import *


def timer(func):
    def wrapper(*args, **kwargs):
        time1 = round(time(), 4)
        print(f'{datetime.now()} - Commencing scraping')
        result = func(*args, **kwargs)
        time2 = round(time(), 4)
        timespan = time2 - time1
        minutes = timespan // 60
        seconds = round(timespan - minutes * 60, 2)
        print(f'{datetime.now()} - Scraping completed in {minutes} m, {seconds} s.')
        print('----------')
        return result
    return wrapper


class ScraperBase:
    async def scrape_job_website(self, location, page_num, query_params=None):
        print(f'Scraping with {self.__class__.__name__}')
        print(f'Scraping for {location}')
        self.output = []
        await self._scrape_job_pages(
                location=location,
                city_name=self.cities[location],
                page_num=page_num,
                query_params=query_params
            )
        print(f'Scraped {len(self.output)} results')
        return {
            'object_list': self.output,
            'last_page': self.last_page_num
        }

    @timer
    def scrape_game_website(self, page_num, query_params=None):
        print(f'Scraping with {self.__class__.__name__}')
        self.output = []
        asyncio.run(self._scrape_game_pages(
            query_params=query_params,
            page_num=page_num,
        ))
        return {
            'object_list': self.output,
            'last_page': self.last_page_num
        }

    def _request_first_page(self, url, session):
        for count in range(5):
            try:
                headers = {'User-Agent': REQUEST_HEADER}
                response = requests.get(url, headers=headers, params=self.params)
                page = response.text
                page = soup(page, 'lxml')
                return page
            except Exception as exeption:
                print(exeption)

    @staticmethod
    def _get_query_string(params):
        return urlencode(params)

    @staticmethod
    def _is_number(line):
        for char in line:
            if not char.isnumeric() and not char in ',. ':
                return False
        return True

    @staticmethod
    def _make_number(line):
        result = ''
        for char in line:
            if char.isnumeric():
                result += char
            if char in '.,':
                result += '.'
        return float(result)

    @staticmethod
    def _parse_price(price):
        if price == None:
            return None
        res = ''
        if price in FREE:
            return float(0)
        for char in price:
            if char.isnumeric() or char == '.':
                res += char
        return float(res)

    def _parse_salary(self, salary):
        if not salary or salary.get_text() == '':
            return None, None, None
        salary = salary.get_text()
        salary_min = ''
        salary_max = ''
        currency = []
        for divider in DIVIDERS:
            if divider in salary:
                salary = salary.split(divider)
        if type(salary) == str:
            salary_min = None
            second_part = salary.split()
        else:
            salary_min = self._make_number(''.join(salary[0]))
            second_part = salary[1].split()
        for item in second_part:
            if self._is_number(item):
                salary_max += item
            else:
                currency.append(item)
        return salary_min, self._make_number(salary_max), ' '.join(currency)

    def _get_job_items(self, offer, location):
        salary_min, salary_max, currency = self._parse_salary(
            self._get_job_salary(offer))
        return {
            'title': self._get_job_title(offer),
            'body': self._get_job_body(offer),
            'location': location,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'currency': currency,
            'employer': self._get_job_employer(offer),
            'link': self._get_job_link(offer),
            'source': self._get_job_source()
        }

    def _get_game_items(self, game):
        price, psplus_price, initial_price = self._get_game_price(game)
        return {
            'title': self._get_game_title(game),
            'price': self._parse_price(price),
            'psplus_price': self._parse_price(psplus_price),
            'initial_price': self._parse_price(initial_price),
            'image': self._get_game_image(game),
            'link': self._get_game_link(game)
        }

    def _add_jobs_to_result(self, jobs, location):
        for job in jobs:
            self.output.append(self._get_job_items(job, location))

    def _add_games_to_result(self, games):
        for game in games:
            self.output.append(self._get_game_items(game))


    def _filter_free_games(game):
        price_is_free = game.get('price') == 0
        psplus_price = game.get('psplus_price')
        psplus_is_free = not psplus_price or psplus_price == 0
        return price_is_free or psplus_is_free

    def _filter_games_output(self,
                             discount_filter=False,
                             psplus_filter=False,
                             free=False):
        if discount_filter:
            self.output = filter(
                lambda game: game.get('initial_price') is not None,
                self.output
            )
        if psplus_filter:
            self.output = filter(
                lambda game: game.get('psplus_price') is not None,
                self.output
            )
        if free:
            self.output = filter(self._filter_free_games, self.output)
        self.output = list(self.output)

    def _set_artificial_last_page(self):
        output_num = len(self.output)
        pages = output_num // GAMES_PER_PAGE
        extra_page = 1 if output_num % GAMES_PER_PAGE > 0 else 0
        self.last_page_num = pages + extra_page

    def _paginate_games_output(self, current_page_num):
        zero_based_index = current_page_num - 1
        start_index = zero_based_index * GAMES_PER_PAGE
        end_index = zero_based_index + GAMES_PER_PAGE
        self.output = self.output[start_index:end_index]

    async def _scrape_job_page(self, url, page_num, location, session):
        print(url)
        # Max of 5 consecutive requests can be made
        # To cover the cases of poor inirial responce, network problems
        # or server error
        for count in range(5):
            try:
                headers = {'User-Agent': REQUEST_HEADER}
                async with session.get(url, headers=headers) as response:
                    page = await response.text()
                    page = soup(page, 'lxml')
                    self.last_page_num = self._get_last_page_num(page)
                    if self.last_page_num < page_num:
                        jobs_list = []
                    else:
                        jobs_list = self._get_jobs_list(page)
                    if response.status == 200:
                        self._add_jobs_to_result(jobs_list, location)
                        break

            except Exception as exeption:
                print(exeption)
        return page

    async def _scrape_job_pages(self, location, city_name, page_num, query_params):
        last_page_num = page_num
        async with aiohttp.ClientSession() as session:
            while page_num <= last_page_num:
                url = self._get_url(city_name, page_num, query_params)
                await self._scrape_job_page(url, page_num, location, session)
                page_num += 1

    async def _scrape_game_page(self, url, page_num, session):
        # Max of 5 consecutive requests can be made
        # To cover the cases of poor inirial responce, network problems
        # or server error
        for count in range(5):
            try:
                headers = {'User-Agent': REQUEST_HEADER}
                async with session.get(url,
                                       headers=headers,
                                       params=self.params) as response:
                    page = await response.text()
                    page = soup(page, 'lxml')
                    base_url = url.split(f'/{page_num}')[0] + '/'
                    if response.status == 200:
                        games_list = self._get_games_list(page)
                        self._add_games_to_result(games_list)
                        # If last page was not explicitly defined
                        # Assign the value of website's own pagination data
                        if not hasattr(self, 'last_page_num'):
                            self.last_page_num = self._get_last_page_num(
                                page,
                                base_url
                            )

                        # If nothing gives an exception,
                        # Regard this page scraping as successfull
                        # And don't send more requests
                        break
            except Exception as exeption:
                print(exeption)

    async def _scrape_game_pages(self, page_num, query_params):
        title = query_params.get('title')
        discount_filter = bool(query_params.get('initial_price'))
        psplus_filter = bool(query_params.get('psplus_price'))
        free = bool(query_params.get('free'))
        any_filters = discount_filter or psplus_filter or free
        async_tasks = []
        async with aiohttp.ClientSession() as session:

            # If title search is filtered, then first get the first page
            # Syncronously and define last page
            # It is needed for accumulating all search results asyncronously
            # And then create artificial pagination from results quantity
            if title and any_filters:
                url = self._get_url(1, query_params)

                # Exclude any query string from url and extract page number
                base_url = url.split('/1')[0] + '/'
                last_page_num = self._get_last_page_num(
                    self._request_first_page(url, session),
                    base_url,
                )
                current_page_num = page_num
                self.last_page_num = last_page_num
                # Set a flag of artificial pagination to True
                # so that output splits itself accordingly
                self.artificial_pagination = True

            # If only Ps Plus offers are selected
            # Get all pages one by one from the list
            elif psplus_filter:
                page_num = 1
                current_page_num = 1
                self.last_page_num = last_page_num = len(PS_STORE_PSPLUS_GAMES)
                self.artificial_pagination = True

            # Else just scrape first page and make pagination
            # In sync with website's pagination
            # Since results ar ethe same
            else:
                last_page_num = page_num

                # Since pagination is in sync with source website,
                # Flag should be set to False so that output is returned as is
                self.artificial_pagination = False
            while page_num <= last_page_num:
                async_task = asyncio.create_task(self._scrape_game_page(
                    self._get_url(page_num, query_params),
                    page_num,
                    session
                ))
                async_tasks.append(async_task)
                page_num += 1

            await asyncio.gather(*async_tasks)
            self._filter_games_output(
                discount_filter=discount_filter,
                psplus_filter=psplus_filter,
                free=free
            )
            # Adjust output according to artificial pagination
            if self.artificial_pagination:
                self._set_artificial_last_page()
                self._paginate_games_output(current_page_num)
