import os
import json
import lxml
from urllib.request import urlopen, Request
from time import time
from datetime import datetime
from bs4 import BeautifulSoup as soup
from .constants import *


def timer(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        time1 = round(time(), 4)
        print(f'{datetime.now()} - Commencing scraping')
        func(*args, **kwargs)
        time2 = round(time(), 4)
        timespan = time2 - time1
        minutes = timespan // 60
        seconds = round(timespan - minutes * 60)
        print(f'{datetime.now()} - Scraping completed in {minutes} m, {seconds} s.')
        print('----------')
    return wrapper


class ScraperBase:

    @timer
    def scrape_job_website(self, page_limit=None):
        print(f'Scraping with {self.__class__.__name__}')
        self.output = []
        for location, city_name in self.cities.items():
            print(f'Scraping for {location}')
            self._scrape_job_pages(
                location=location,
                city_name=city_name,
                page_limit=page_limit)
        self._save_results_to_json(self.filename)

    @timer
    def scrape_game_website(self, page_limit=None):
        print(f'Scraping with {self.__class__.__name__}')
        self.output = []
        self._scrape_game_pages(page_limit=page_limit)
        self._save_results_to_json(self.filename)

    @staticmethod
    def _request_page(url, pagenum=1):
        url = url + str(pagenum)
        for count in range(5):
            try:
                request = Request(url, headers={'User-Agent': REQUEST_HEADER})
                with urlopen(request) as response:
                    page = response.read()
                    page = soup(page, 'lxml')
                    return page
            except:
                pass


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
        for job in jobs:
            self.output.append(self._get_job_items(job, location))

    def _add_games_to_result(self, games):
        for game in games:
            self.output.append(self._get_game_items(game))

    def _scrape_job_pages(self, location, city_name, page_limit):
        url = self._get_url(city_name)
        self.last_page_num = self._get_last_page_num(self._request_page(url))
        page_num = 1
        while True:
            print(f'Scraping page #{page_num}')
            if page_num > self.last_page_num or (page_limit and page_num > page_limit):
                return
            page = self._request_page(url, page_num)
            self._add_jobs_to_result(self._get_jobs_list(page), location)
            page_num += 1

    def _scrape_game_pages(self, page_limit):
        url = self._get_url()
        self.last_page_num = self._get_last_page_num(self._request_page(url))
        page_num = 1
        while True:
            print(f'Scraping page #{page_num}')
            if page_num > self.last_page_num or (page_limit and page_num > page_limit):
                return
            page = self._request_page(url, page_num)
            self._add_games_to_result(self._get_games_list(page))
            page_num += 1
