import asyncio
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
        last = page.find('div', class_='paging')
        if last: last = last.find_all('a')[-1]
        return int(last.get_text()) if last else 1

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
    def _check_end_of_pagination(self, page):
        if page.find('ul', class_='pagination'):
            return bool(page.find('li', class_='next disabled'))
        else:
            return True
        return False

    def _scrape_job_pages(self, location, city_name, page_limit):
        for job_type in JOBISCOMUA_CATEGORIES:
            url = f'{self._get_url(city_name)}{job_type}?page='
            page_num = 1
            while True:
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

    def _get_url(self, city_name, page_num, query_params):
        DEFAULT_MIN_SALARY = '1'
        DEFAULT_MAX_SALARY = '1000000'
        title = self._convert_title(query_params.get('title')) if query_params else ''
        salary_min = query_params.get('salary_min')
        salary_max = query_params.get('salary_max')
        with_salary = query_params.get('with_salary')
        salary = ''
        if salary_min or salary_max or with_salary:
            salary_min = salary_min if salary_min else DEFAULT_MIN_SALARY
            salary_max = salary_max if salary_max else DEFAULT_MAX_SALARY
            salary = f'?salary={salary_min},{salary_max}'
        return f'{JOBSUA_LINK}/{city_name}/rabota-{title}{salary}/page-{page_num}'

    @staticmethod
    def _convert_title(title):
        return '-'.join(title.lower().split()) if title else ''

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('div', class_='b-vacancy__pages-title')
        if last: last = last.span
        if last: last = last.find_all('b')
        return int(last[1].get_text()) if last else 1

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

    def _get_url(self, city_name, page_num, query_params):
        DEFAULT_MIN_SALARY = '1'
        title = self._convert_title(query_params.get('title')) if query_params else ''
        salary_min = query_params.get('salary_min')
        with_salary = query_params.get('with_salary')
        salary = ''
        page_num = f'p={page_num}'
        if salary_min or with_salary:
            salary_min = salary_min if salary_min else DEFAULT_MIN_SALARY
            salary = f'salary={salary_min}&'
        return f'{JOOBLEORG_LINK}/работа-{title}/{city_name}?{salary}{page_num}'

    @staticmethod
    def _convert_title(title):
        return '-'.join(title.lower().split()) if title else ''

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('div', class_='paging')
        if last: last = last.find_all('a')
        return int(last[-1].get_text()) if last else 1

    @staticmethod
    def _get_jobs_list(page):
        jobs = page.find('div', id='jobs_list__page')
        return jobs.find_all('div', class_='vacancy_wrapper') if jobs else []

    @staticmethod
    def _get_job_title(offer):
        return offer.find(
            'h2',id='h2Position', class_='position').get_text()

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
        return offer.find('div', class_='top-wr').a['href'].split('ckey=')[0]

    @staticmethod
    def _get_job_source():
        return JOOBLEORG_BASELINK

    # TODO: change this method to allow scrape maximum amount of pages
    #
    # def _scrape_job_pages(self, location, city_name, page_limit):
    #     url = self._get_url(city_name)
    #     page_num = 1
    #     while True:
    #         page = self._request_page(url, page_num)
    #         self.last_page_num = self._get_last_page_num(page)
    #         if page_num > self.last_page_num or (page_limit and page_num > page_limit):
    #             break
    #         self._add_jobs_to_result(self._get_jobs_list(page), location)
    #         page_num += 1


class NovarobotaScraper(ScraperBase):
    def __init__(self):
        self.cities = NOVAROBOTAUA_CITIES

    def _get_url(self, city_name, page_num, query_params):
        DEFAULT_MIN_SALARY = '1'
        DEFAULT_MAX_SALARY = '1000000'
        title = self._convert_title(query_params.get('title')) if query_params else ''
        salary_min = query_params.get('salary_min')
        salary_max = query_params.get('salary_max')
        with_salary = query_params.get('with_salary')
        salary = ''
        page_num = f'page={page_num}'
        if salary_min or salary_max or with_salary:
            salary_min = salary_min if salary_min else DEFAULT_MIN_SALARY
            salary_max = salary_max if salary_max else DEFAULT_MAX_SALARY
            salary = f'salary={salary_min}_{salary_max}&'
        return f'{NOVAROBOTAUA_LINK}/{title}/{city_name}?{salary}{page_num}'

    @staticmethod
    def _convert_title(title):
        return '+'.join(title.lower().split()) if title else ''

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('ul', class_='pagination')
        if last: last = last.find('ul', class_='pagination')
        if last: last = last.find_all('li')
        if last: last = last[-2].get_text()
        return int(last) if last else 1

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

    def _get_url(self, city_name, page_num, query_params):
        title = self._convert_title(query_params.get('title')) if query_params else ''
        salary_min = query_params.get('salary_min')
        with_salary = query_params.get('with_salary')
        page_num = f'page={page_num}'
        salary = f'salary={salary_min}&currencyId=1&' if salary_min else ''
        with_salary = 'salaryType=1&' if with_salary else ''
        return f'{RABOTAUA_LINK}?keyWords={title}{city_name}{salary}{page_num}'

    @staticmethod
    def _convert_title(title):
        return '+'.join(title.lower().split()) + '&' if title else ''

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('dd', class_='nextbtn')
        if last: last = last.previous_sibling
        if last: last = last.find('a')
        return int(last.get_text()) if last else 1

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


class RabotaAPIScraper(ScraperBase):
    def __init__(self):
        self.cities = RABOTAUA_API_CITIES

    def _get_url(self, city_name, page_num, query_params):
        title = self._convert_title(query_params.get('title')) if query_params else ''
        salary_min = query_params.get('salary_min')
        with_salary = query_params.get('with_salary')
        page_num = f'page={page_num}'
        salary = f'salary={salary_min}&' if salary_min else ''
        with_salary = 'noSalary=false&' if with_salary else ''
        return f'{RABOTAUA_API_LINK}?keyWords={title}&{city_name}{salary}{page_num}'

    @staticmethod
    def _convert_title(title):
        return '+'.join(title.lower().split()) if title else ''

    def _parse_salary(self, salary):
        return None, salary, 'UAH'

    @staticmethod
    def _get_last_page_num(response):
        total_results = response["total"]
        if total_results == 0:
            return 1
        results_per_page = response["count"]
        return total_results // results_per_page

    @staticmethod
    def _get_jobs_list(response): return response["documents"]

    @staticmethod
    def _get_job_title(offer): return offer["name"]

    @staticmethod
    def _get_job_body(offer): return offer["shortDescription"]

    @staticmethod
    def _get_job_salary(offer):
        return offer["salary"] if offer["salary"] != 0 else None

    @staticmethod
    def _get_job_employer(offer):
        return offer["companyName"] if offer["companyName"] else None

    @staticmethod
    def _get_job_link(offer):
        company_id = offer["notebookId"]
        offer_id = offer["id"]
        return f'https://rabota.ua/ua/company{company_id}/vacancy{offer_id}'

    @staticmethod
    def _get_job_source():
        return RABOTAUA_BASELINK

    async def _scrape_job_page(self, url, page_num, location, session):
        # Max of 5 consecutive requests can be made
        # To cover the cases of poor inirial responce, network problems
        # or server error
        for count in range(5):
            try:
                headers = {'Accept': 'application/json'}
                async with session.get(url, headers=headers) as response:
                    response_data = await response.json()
                    self.last_page_num = self._get_last_page_num(response_data)
                    if self.last_page_num < page_num:
                        jobs_list = []
                    else:
                        jobs_list = self._get_jobs_list(response_data)
                    if response.status == 200:
                        self._add_jobs_to_result(jobs_list, location)
                        break
            except Exception as exeption:
                print(f'Scraping exception: {exeption}')
        return response_data

    async def _scrape_job_pages(self, location, city_name, page_num, query_params):
        last_page_num = self.last_page_num = page_num
        async with aiohttp.ClientSession() as session:
            while page_num <= last_page_num:
                url = self._get_url(city_name, page_num, query_params)
                await self._scrape_job_page(url, page_num, location, session)
                page_num += 1



class TrudScraper(ScraperBase):
    def __init__(self):
        self.cities = TRUDUA_CITIES

    def _get_url(self, city_name, page_num, query_params):
        DEFAULT_MIN_SALARY = '1'
        title = self._convert_title(query_params.get('title')) if query_params else ''
        salary_min = query_params.get('salary_min')
        with_salary = query_params.get('with_salary')
        salary = ''
        page_num = f'/page/{page_num}' if page_num != 1 else ''
        if salary_min or with_salary:
            salary_min = salary_min if salary_min else DEFAULT_MIN_SALARY
            salary = f'/salary/{salary_min}'
        if city_name:
            return f'{TRUDUA_LINK_CITY}/{city_name}/q/{title}{salary}{page_num}.html'
        return f'{TRUDUA_LINK}/{title}{salary}{page_num}.html'

    @staticmethod
    def _convert_title(title):
        return '+'.join(title.lower().split()) if title else ''

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('div', class_='yiiPager')
        if last:
            last = last.find('a', class_='next-p')['href'].split('/')[-1][:-5]
        else:
            last = '1'
        return int(last)

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

    async def _scrape_job_pages(self, location, city_name, page_num, query_params):
        last_page_num = page_num
        async with aiohttp.ClientSession() as session:
            while page_num <= last_page_num:
                url = self._get_url(city_name, page_num, query_params)
                page = await self._scrape_job_page(url, page_num, location, session)
                self.last_page_num = page_num
                if page and page.find('span', class_='next-p disabled') is not None:
                    break
                page_num += 1


class WorkScraper(ScraperBase):
    def __init__(self):
        self.cities = WORKUA_CITIES

    def _get_url(self, city_name, page_num, query_params):
        SALARY_OPTIONS = (0, 3000, 5000, 7000, 10000, 15000, 20000, 30000, 50000)

        title = self._convert_title(query_params.get('title')) if query_params else ''
        salary_min = query_params.get('salary_min')
        salary_max = query_params.get('salary_max')

        if salary_min:
            for index in range(1, len(SALARY_OPTIONS)):
                if SALARY_OPTIONS[index] > int(salary_min):
                    salary_min = f'salaryfrom={index}&'
                    break
        else:
            salary_min = ''

        if salary_max and int(salary_max) > SALARY_OPTIONS[-1]:
            salary_max = ''
        elif salary_max:
            for index in range(1, len(SALARY_OPTIONS)):
                if SALARY_OPTIONS[index] > int(salary_max):
                    salary_max = f'salaryto={index + 1}&'
                    break
        else:
            salary_max = ''

        page_num = f'?page={page_num}' if page_num else ''
        city_name = f'{city_name}-' if city_name else ''
        return f'{WORKUA_LINK}{city_name}{title}/?{salary_min}{salary_max}/{page_num}'

    @staticmethod
    def _convert_title(title):
        return '+'.join(title.lower().split()) if title else ''

    @staticmethod
    def _get_last_page_num(page):
        last = page.find('ul', class_='pagination pagination-small visible-xs-block')
        if last: last = last.find('span', class_='text-default')
        return int(last.get_text().split()[-1]) if last else 1

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
        tag = offer.h2.next_sibling.next_sibling
        if tag.get('class'):
            return None
        return tag.b

    @staticmethod
    def _get_job_employer(offer):
        return offer.find('div', class_='add-top-xs').b.get_text()

    @staticmethod
    def _get_job_link(offer):
        return WORKUA_BASELINK + offer.h2.a['href']

    @staticmethod
    def _get_job_source():
        return WORKUA_BASELINK


class JobsSitesScraper:
    async def _scrape_websites(self, location, page_num, query_params):
        async_tasks = []
        websites = [
            # TODO: Include categories to job search
            # Otherwise Jobis will not work
            #
            # JobisScraper().scrape_job_website,
            JobsScraper(),
            JoobleScraper(),
            NovarobotaScraper(),
            # RabotaScraper(),
            RabotaAPIScraper(),
            TrudScraper(),
            WorkScraper()
        ]
        if location:
            for website in websites:
                async_task = asyncio.create_task(website.scrape_job_website(
                    location,
                    page_num,
                    query_params
                ))
                async_tasks.append(async_task)
        else:
            for website in websites:
                for location in website.cities.keys():
                    async_task = asyncio.create_task(website.scrape_job_website(
                        location,
                        page_num,
                        query_params
                    ))
                    async_tasks.append(async_task)
        return await asyncio.gather(*async_tasks)

    @staticmethod
    def _adjust_results_number(results):
        object_list = []
        last_page_list = []
        for item in results:
            object_list.extend(item['object_list'])
            last_page_list.append(item['last_page'])
        return {
            'object_list': object_list,
            'last_page': max(last_page_list)
        }

    # @timer
    def scrape_websites(self, location, page_num, query_params):
        results = asyncio.run(
            self._scrape_websites(location, page_num, query_params),
            debug=True
        )
        return self._adjust_results_number(results)
