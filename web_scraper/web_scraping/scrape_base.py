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


# For gererating url-safe query strings:
# quote('query string', safe='')


def timer(func):
    def wrapper(*args, **kwargs):
        time1 = round(time(), 4)
        print(f'{datetime.now()} - Commencing scraping')
        result = func(*args, **kwargs)
        time2 = round(time(), 4)
        timespan = time2 - time1
        minutes = timespan // 60
        seconds = round(timespan - minutes * 60)
        print(f'{datetime.now()} - Scraping completed in {minutes} m, {seconds} s.')
        print('----------')
        return result
    return wrapper


class ScraperBase:
    @timer
    def scrape_job_website(self, query_params=None, page_limit=None):
        print(f'Scraping with {self.__class__.__name__}')
        self.output = []
        for location, city_name in self.cities.items():
            print(f'Scraping for {location}')
            asyncio.run(self._scrape_job_pages(
                location=location,
                city_name=city_name,
                page_limit=page_limit))
        print(f'Scraped {len(self.output)} results')
        # print('Finished scraping, saving data to .json file')
        # self._save_results_to_json(self.filename)

    @timer
    def scrape_game_website(self, page_num, query_params=None, page_limit=None):
        print(f'Scraping with {self.__class__.__name__}')
        self.output = []
        asyncio.run(self._scrape_game_pages(
            query_params=query_params,
            page_num=page_num,
            page_limit=page_limit
        ))
        return {
            'object_list': self.output,
            'last_page': self.last_page_num
        }
        # print('Finished scraping, saving data to .json file')
        # self._save_results_to_json(self.filename)

    @staticmethod
    async def _request_page(url, pagenum, session):
        url = url + str(pagenum)
        for count in range(5):
            try:
                headers = {'User-Agent': REQUEST_HEADER}
                async with session.get(url, headers=headers) as response:
                    page = await response.read()
                    page = soup(page, 'lxml')
                    return page
            except:
                pass

    @staticmethod
    def _request_first_page(url):
        for count in range(5):
            try:
                session = requests.session()
                headers = {'User-Agent': REQUEST_HEADER}
                with session.get(url, headers=headers) as response:
                    page = soup(response.text, 'lxml')
                    return page
            except Exception as exeption:
                print(exeption)


    @staticmethod
    def _make_url_safe(query):
        return quote(query, safe='')

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

    def _save_results_to_json(self, filename):
        with open(filename, 'w+') as file:
            json.dump(self.output, file)
            file.close()

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
        # print('Adding jobs to results list')
        # print(f'Current results length: {len(self.output)}')
        for job in jobs:
            self.output.append(self._get_job_items(job, location))

    def _add_games_to_result(self, games):
        for game in games:
            self.output.append(self._get_game_items(game))

    async def _scrape_job_page(self, url, page_num, location, session):
        # print(f'{location} Scraping page #{page_num}')
        url = url + str(page_num)
        for count in range(5):
            try:
                await asyncio.sleep(random() * 100)
                headers = {'User-Agent': REQUEST_HEADER}
                async with session.get(url, headers=headers) as response:
                    await asyncio.sleep(random() * 100)
                    print(f'--#{page_num} Parsing the page')
                    page = await response.text()
                    page = soup(page, 'lxml')
                    jobs_list = self._get_jobs_list(page)
                    if len(jobs_list) == 0:
                        print(f'--> Page#{page_num} "{response.status}" CRASHED :D')
                    else:
                        print(f'-> Page#{page_num} "{response.status}" SUCCESSFULL')
                        self._add_jobs_to_result(jobs_list, location)
                        break
            except Exception as exeption:
                print(exeption)

    async def _scrape_job_pages(self, location, city_name, page_limit):
        url = self._get_url(city_name)
        self.last_page_num = self._get_last_page_num(self._request_first_page(url))
        page_num = 1
        async_tasks = []
        async with aiohttp.ClientSession() as session:
            while not (page_num > self.last_page_num or (page_limit and page_num > page_limit)):
                # print(f'Creating task No {page_num}')
                async_task = asyncio.create_task(self._scrape_job_page(url, page_num, location, session))
                async_tasks.append(async_task)
                # print(f'Scraping page #{page_num}')
                # page = self._request_page(url, page_num)
                # self._add_jobs_to_result(self._get_jobs_list(page), location)
                page_num += 1
            # print('Gathering all created tasks')
            await asyncio.gather(*async_tasks)


    async def _scrape_game_page(self, url, page_num, session):
        print(url)
        for count in range(5):
            try:
                headers = {'User-Agent': REQUEST_HEADER}
                async with session.get(url, headers=headers) as response:
                    page = await response.read()
                    page = soup(page, 'lxml')
                    games_list = self._get_games_list(page)
                    self._add_games_to_result(games_list)
                    break
            except Exception as exeption:
                print(exeption)

    async def _scrape_game_pages(self, page_num, query_params, page_limit):
        async_tasks = []
        async with aiohttp.ClientSession() as session:
            url = self._get_url(1, query_params)
            base_url = url.split('/1')[0] + '/'
            self.last_page_num = self._get_last_page_num(
                self._request_first_page(url),
                base_url
            )
            page_num = page_num if page_num else 1
            while not (page_num > self.last_page_num or (page_limit and page_num > page_limit)):
                async_task = asyncio.create_task(self._scrape_game_page(
                    self._get_url(page_num, query_params),
                    page_num,
                    session
                ))
                async_tasks.append(async_task)
                page_num += 1
            await asyncio.gather(*async_tasks)
