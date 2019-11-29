from .scrape_base import *


class JobisScraper(ScraperBase):

    def __init__(self):
        self.cities = JOBISCOMUA_CITIES
        self.filename = JOBISCOMUA_FILE

    @staticmethod
    def _get_url(city_name):
        return f'{JOBISCOMUA_LINK}{city_name}'

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('div', class_='paging').find_all('a')[-1]
        return int(last.get_text()) if last else None

    @staticmethod
    def _get_jobs_list(page):
        offers = page.find_all('div', class_='list-group-item')
        return [offer for offer in offers if offer.has_attr('id')]

    @staticmethod
    def _get_job_title(offer):
        return offer.find('h3').find('a').get_text()

    @staticmethod
    def _get_job_body(offer):
        return offer.find('blockquote').get_text().split(' подробнее')[0]

    @staticmethod
    def _get_job_salary(offer):
        return offer.find('p', class_='text-danger')

    @staticmethod
    def _get_job_employer(offer):
        employer_tag = offer.find('strong')
        return employer_tag.get_text().strip() if employer_tag else None

    @staticmethod
    def _get_job_link(offer):
        return JOBISCOMUA_BASELINK + offer.find('h3').a['href']

    @staticmethod
    def _get_job_source():
        return JOBISCOMUA_BASELINK

    @staticmethod
    def _check_end_of_pagination(page):
        if page.find('ul', class_='pagination'):
            if page.find('li', class_='next disabled'):
                return True
        else:
            return True
        return False

    def _scrape_job_pages(self, location, city_name, page_limit):
        for job_type in JOBISCOMUA_CATEGORIES:
            url = f'{self._get_url(city_name)}{job_type}?page='
            page_num = 1
            while True:
                print(f'Scraping page #{page_num}')
                if page_limit and page_num > page_limit:
                    break
                page = self._request_page(url, page_num)
                if page.find('div', class_='alert-danger alert fade in'):
                    break
                jobs_list = self._get_jobs_list(page)
                if not jobs_list:
                    break
                self._add_jobs_to_result(jobs_list, location)
                if self._check_end_of_pagination(page):
                    break
                page_num += 1


class JobsScraper(ScraperBase):

    def __init__(self):
        self.cities = JOBSUA_CITIES
        self.filename = JOBSUA_FILE

    @staticmethod
    def _get_url(city_name):
        return f'{JOBSUA_LINK}{city_name}/page-'

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('div', class_='b-vacancy__pages-title').span.find_all('b')
        return int(last[1].get_text()) if last else None

    @staticmethod
    def _get_jobs_list(page):
        offers = page.find_all('li', class_='b-vacancy__item js-item_list')
        return [offer for offer in offers if offer.has_attr('id')]

    @staticmethod
    def _get_job_title(offer):
        return offer.find(
            'div', class_='b-vacancy__top-inner').find(
            'a', class_='b-vacancy__top__title').get_text()

    @staticmethod
    def _get_job_body(offer):
        body = ''
        for requirement in offer.find_all('div', class_='b-vacancy__tech__item'):
            if requirement.find('span', class_='caption'):
                body += requirement.find(
                    'span', class_='caption').get_text() + ' ' + requirement.find(
                    'span', class_='black-text').get_text() + '. '
        body += '\n'
        for paragraph in offer.find('div', class_='grey-light').find_all('p'):
            body += paragraph.get_text()
        return body.strip()

    @staticmethod
    def _get_job_salary(offer):
        return offer.find('span', class_='b-vacancy__top__pay')

    @staticmethod
    def _get_job_employer(offer):
        employer_tag = offer.find('span', class_='link__hidden')
        return employer_tag.get_text().strip() if employer_tag else None

    @staticmethod
    def _get_job_link(offer):
        return offer.find('div', class_='b-vacancy__top-inner').a['href']

    @staticmethod
    def _get_job_source():
        return JOBSUA_BASELINK


class JoobleScraper(ScraperBase):

    def __init__(self):
        self.cities = JOOBLEORG_CITIES
        self.filename = JOOBLEORG_FILE

    @staticmethod
    def _get_url(city_name):
        return f'{JOOBLEORG_LINK}{city_name}?p='

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('div', class_='paging').find_all('a')
        return int(last[-1].get_text()) if last else None

    @staticmethod
    def _get_jobs_list(page):
        return page.find(
            'div', id='jobs_list__page').find_all('div', class_='vacancy_wrapper')

    @staticmethod
    def _get_job_title(offer):
        return offer.find(
            'h2',id='h2Position', class_='position').find('span').get_text()

    @staticmethod
    def _get_job_body(offer):
        return offer.find('span', class_='description').get_text()

    @staticmethod
    def _get_job_salary(offer):
        return offer.find('span', class_='salary')

    @staticmethod
    def _get_job_employer(offer):
        employer_tag = offer.find('span', class_='gray_text company-name')
        return employer_tag.get_text().strip() if employer_tag else None

    @staticmethod
    def _get_job_link(offer):
        return offer.find('div', class_='top-wr').a['href']

    @staticmethod
    def _get_job_source():
        return JOOBLEORG_BASELINK

    def _scrape_job_pages(self, location, city_name, page_limit):
        url = self._get_url(city_name)
        page_num = 1
        while True:
            print(f'Scraping page #{page_num}')
            page = self._request_page(url, page_num)
            self.last_page_num = self._get_last_page_num(page)
            if page_num > self.last_page_num or (page_limit and page_num > page_limit):
                return
            self._add_jobs_to_result(self._get_jobs_list(page), location)
            page_num += 1


class NovarobotaScraper(ScraperBase):

    def __init__(self):
        self.cities = NOVAROBOTAUA_CITIES
        self.filename = NOVAROBOTAUA_FILE

    @staticmethod
    def _get_url(city_name):
        return f'{NOVAROBOTAUA_LINK}{city_name}?page='

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('ul',
            class_='pagination').find('ul',
            class_='pagination').find_all('li')
        return int(last[-2].get_text()) if last else None

    @staticmethod
    def _get_jobs_list(page):
        return page.find_all('div', class_='vacancy')

    @staticmethod
    def _get_job_title(offer):
        return offer.find('a', class_='title').get_text()

    @staticmethod
    def _get_job_body(offer):
        body_tag = offer.find('div', class_='price').next_sibling.next_sibling
        return body_tag.get_text().strip()

    @staticmethod
    def _get_job_salary(offer):
        return offer.find('div', class_='price')

    @staticmethod
    def _get_job_employer(offer):
        tag = offer.find('div', class_='info')
        return tag.get_text().strip().split('\n')[0] if tag else None

    @staticmethod
    def _get_job_link(offer):
        return NOVAROBOTAUA_BASELINK + offer.find('div', class_='col-xs-12').a['href']

    @staticmethod
    def _get_job_source():
        return NOVAROBOTAUA_BASELINK


class RabotaScraper(ScraperBase):

    def __init__(self):
        self.cities = RABOTAUA_CITIES
        self.filename = RABOTAUA_FILE

    @staticmethod
    def _get_url(city_name):
        return f'{RABOTAUA_LINK}{city_name}&pg='

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('dd', class_='nextbtn').previous_sibling.find('a')
        return int(last.get_text()) if last else None

    @staticmethod
    def _get_jobs_list(page):
        return page.find_all('article', class_='f-vacancylist-vacancyblock')

    @staticmethod
    def _get_job_title(offer):
        return offer.find(
            'h3', class_='f-vacancylist-vacancytitle').find(
            'a', class_='f-visited-enable ga_listing').get_text().split('\n')[0]

    @staticmethod
    def _get_job_body(offer):
        return offer.find(
            'p', class_='f-vacancylist-shortdescr').get_text().strip('\n')

    @staticmethod
    def _get_job_salary(offer):
        return offer.find('p', class_='fd-beefy-soldier -price')

    @staticmethod
    def _get_job_employer(offer):
        employer_tag = offer.find('p', class_='f-vacancylist-companyname').a
        return employer_tag.get_text().split('\n')[0] if employer_tag else None

    @staticmethod
    def _get_job_link(offer):
        return RABOTAUA_BASELINK + offer.find(
            'h3', class_='f-vacancylist-vacancytitle').a['href']

    @staticmethod
    def _get_job_source():
        return RABOTAUA_BASELINK


class TrudScraper(ScraperBase):

    def __init__(self):
        self.cities = TRUDUA_CITIES
        self.filename = TRUDUA_FILE

    @staticmethod
    def _get_url(city_name):
        return f'{TRUDUA_LINK}{city_name}/page/'

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('div', class_='yiiPager')
        return last.find('a', class_='next-p') if last else None

    @staticmethod
    def _get_jobs_list(page):
        return page.find_all('div', class_='result-unit')

    @staticmethod
    def _get_job_title(offer):
        return offer.find('div', class_='titl-r').find('a').get_text()

    @staticmethod
    def _get_job_body(offer):
        return offer.find('div', class_='descr-r').find('a').get_text()

    @staticmethod
    def _get_job_salary(offer):
        return offer.find('div', class_='salary')

    @staticmethod
    def _get_job_employer(offer):
        employer_tag = offer.find('div', class_='institution').find('a')
        return employer_tag.get_text().strip() if employer_tag else None

    @staticmethod
    def _get_job_link(offer):
        return TRUDUA_BASELINK + offer.find('div', class_='titl-r').a['href']

    @staticmethod
    def _get_job_source():
        return TRUDUA_BASELINK

    def _scrape_job_pages(self, location, city_name, page_limit):
        url = self._get_url(city_name)[:-5]
        page_num = 1
        while True:
            print(f'Scraping page #{page_num}')
            if page_limit and page_num > page_limit:
                return
            if page_num == 1:
                url = f'https://trud.ua/state/{city_name}/'
            else:
                url = self._get_url(city_name)
            page = self._request_page(url, page_num)
            self._add_jobs_to_result(self._get_jobs_list(page), location)
            end = page.find('span', class_='next-p disabled')
            if end is not None:
                return
            page_num += 1


class WorkScraper(ScraperBase):

    def __init__(self):
        self.cities = WORKUA_CITIES
        self.filename = WORKUA_FILE

    @staticmethod
    def _get_url(city_name):
        return f'{WORKUA_LINK}{city_name}/?ss=1&page='

    @staticmethod
    def _get_last_page_num(page):
        last = page.find(
            'ul', class_='pagination pagination-small visible-xs-block').find(
            'span', class_='text-default')
        return int(last.get_text().split()[-1]) if last else None

    @staticmethod
    def _get_jobs_list(page):
        return page.find_all('div', class_='job-link')

    @staticmethod
    def _get_job_title(offer):
        return offer.h2.a['title'].split(', ')[0]

    @staticmethod
    def _get_job_body(offer):
        return offer.find(class_='overflow').get_text().strip('\n')

    @staticmethod
    def _get_job_salary(offer):
        return offer.h2.find('span', class_='nowrap')

    @staticmethod
    def _get_job_employer(offer):
        return offer.b.get_text().strip() if offer.b else None

    @staticmethod
    def _get_job_link(offer):
        return WORKUA_BASELINK + offer.h2.a['href']

    @staticmethod
    def _get_job_source():
        return WORKUA_BASELINK
